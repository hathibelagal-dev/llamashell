from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import TextStreamer
from transformers.utils import get_json_schema

class LLM:
    system_message = """You are a very helpful assistant and programmer. You like to keep your answers short and to the point because you are very confident."""

    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = "mps" if torch.backends.mps.is_available() else self.device
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.bfloat16 if self.device != "mps" else torch.float16,
        ).to(self.device)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.streamer.on_finalized_text = lambda text, stream_end=None: self.handle_finalized_text(text, stream_end)

        self.chat = [
            {"role": "system", "content": self.system_message}            
        ]
        self.original_chat = self.chat.copy()
        self.full_text = ""

        self.model.eval()

    def add_message(self, role, content):
        self.chat.append({
            "role": role, "content": content
        })

    def handle_finalized_text(self, text, stream_end):
        print(text, end="", flush=True)
        self.full_text += text
        if stream_end:
            self.add_message(role="assistant", content=self.full_text)
            self.full_text = ""

    def send_message(self, message):
        self.add_message(role="user", content=message)
        inputs = self.tokenizer.apply_chat_template(self.chat, tools=None, add_generation_prompt=True, return_dict=True, return_tensors="pt")
        inputs = inputs.to(self.device)
        inputs = {k: v for k, v in inputs.items()}
        self.model.generate(**inputs, max_new_tokens=2048, 
                do_sample=True, top_p=0.95, temperature=0.99,
                pad_token_id=self.tokenizer.eos_token_id,
                streamer=self.streamer
        )

    