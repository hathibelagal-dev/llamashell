from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLM:

    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.bfloat16, device_map="auto"
        )
        self.model.eval()

    def send_message(self, message):
        chat = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]

    