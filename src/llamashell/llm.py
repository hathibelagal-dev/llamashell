from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from . import tools
from transformers.utils import get_json_schema

class LLM:
    system_message = """
    You are a very helpful assistant and programmer. You like to keep your answers short and to the point because you are very confident.
    """

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
        self.model.eval()

    def get_tools(self):
        _tools = [getattr(tools, tool) for tool in dir(tools) if tool.startswith("tool_")]
        output = []
        for tool in _tools:
            schema = get_json_schema(tool)
            output.append(schema)
        return output

    def send_message(self, message, use_tools = False):
        chat = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": message},
        ]
        inputs = self.tokenizer.apply_chat_template(chat, tools=self.get_tools() if use_tools else None, add_generation_prompt=True, return_dict=True, return_tensors="pt")
        inputs = inputs.to(self.device)
        inputs = {k: v for k, v in inputs.items()}
        outputs = self.model.generate(**inputs, max_new_tokens=1024, 
                do_sample=True, top_p=0.95, temperature=0.99,
                pad_token_id=self.tokenizer.eos_token_id,
        )
        output = self.tokenizer.decode(outputs[0])
        return output

    