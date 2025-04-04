
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
    def _callback(self, x, *, buffer, done_generating):
        # TODO: Refactor this callback to only include basic functionality & remove print statements
        #period_id = self.tokenizer.encode(".")[0]
        buffer.append(
            #self.tokenizer.decode([period_id] + x.tolist())[1:]
            #self.tokenizer.decode([period_id, x.item()])[1:]
            self.tokenizer.decode([x.item()])
        )  # I think this results in the first output token being dropped from the display which is wrong.
        if x.item() == self.eot_id:
            done_generating = True
            buffer = buffer[:-1]  # drop the eot_id from the output buffer
        if len(buffer) == 4 or done_generating:
            print("".join(buffer), end="", flush=True)
            buffer.clear()
    def generate():
    def decode_one_token(
        self,
        model,
        x: torch.Tensor,
        input_pos: torch.Tensor,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        assert input_pos.shape[-1] == 1
        x = x.view(1, -1)
        logits = model(x, input_pos)
        if self.generate_full_logit:
            logits = logits[:, -1, :]
        return self.sample(logits, self.temperature, self.top_k)
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
        