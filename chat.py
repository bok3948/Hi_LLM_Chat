
import torch
import logging

class chatbot:
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def sample(
        self,
        logits,
        temperature: float = 0,
        top_k: Optional[int] = None,
    ):
        if temperature == 0:
            
            _, idx_next = torch.topk(logits, k=1, dim=-1)
            if idx_next.dim() == 0:
                idx_next = idx_next.unsqueeze(0)  # shape=(1,)
            return (idx_next, None)
        probs = self.logits_to_probs(logits[0, -1], temperature, top_k)
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
        