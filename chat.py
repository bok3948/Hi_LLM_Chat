
import torch
import logging

class chatbot:
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
    def generate():
    def decode_n_tokens():
    def prefill(
        self,
        model,
        x: torch.Tensor,
        input_pos: torch.Tensor,
    ) -> torch.Tensor:
        logger.debug("x: %s, input_pos: %s", x, input_pos)
        logits = model(x, input_pos)
        if self.generate_full_logit:
            logits = logits[:, -1, :]
        return self.sample(logits)[0]
    def chat():
        