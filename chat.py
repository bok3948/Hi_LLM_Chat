
import torch
import logging

class _ChatFormatter(ABC):


    MESSAGE_TYPE = Dict[str, Union[str, List[Dict[str, str]]]]

    DIALOG_TYPE = List[MESSAGE_TYPE]

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @abstractmethod
    def encode_dialog_prompt(
        self,
        dialog: DIALOG_TYPE,
        add_generation_prompt: bool = True,
    ) -> List[int]:
        """Encode a sequence of messages into a sequence of token IDs, including
        the chat template

        Args:
            dialog (DIALOG_TYPE): The sequence of dialog messages to encode.
                This will be the additional messages on top of those that have
                already been processed.
            add_generation_prompt (bool): Whether to include a generation prompt
                at the end of the encoded sequence.

        Returns:
            List[int]: A list of token IDs representing the encoded prompt.
        """

class Llama3ChatFormatter(_ChatFormatter):
    """Format a chat prompt using special tokens to demarcate roles and messages.

    Refer to the LLaMA3 documentation for more details https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3

    """

    def _encode_header(self, role) -> List[int]:
        tokens = []
        tokens.append(self.tokenizer.special_tokens["<|start_header_id|>"])
        tokens.extend(self.tokenizer.encode(role, bos=False, eos=False))
        tokens.append(self.tokenizer.special_tokens["<|end_header_id|>"])
        tokens.extend(self.tokenizer.encode("\n\n", bos=False, eos=False))
        return tokens

    def _encode_message(self, message: _ChatFormatter.MESSAGE_TYPE) -> List[int]:
        tokens = self._encode_header(message["role"])
        if isinstance(message["content"], str):
            tokens.extend(
                self.tokenizer.encode(message["content"], bos=False, eos=False)
            )
        elif isinstance(message["content"], list):
            for content in message["content"]:
                if content["type"] == "text":
                    tokens.extend(
                        self.tokenizer.encode(content["text"], bos=False, eos=False)
                    )

        tokens.append(self.tokenizer.special_tokens["<|eot_id|>"])
        return tokens

    def encode_dialog_prompt(
        self,
        dialog: _ChatFormatter.DIALOG_TYPE,
        add_generation_prompt: bool = True,
    ) -> List[int]:
        tokens = []
        tokens.append(self.tokenizer.special_tokens["<|begin_of_text|>"])
        for message in dialog:
            tokens.extend(self._encode_message(message))
        # Add the start of an assistant message for the model to complete.
        if add_generation_prompt and dialog and dialog[-1]["role"] != "assistant":
            tokens.extend(self._encode_header("assistant")) # Pass role directly as a string
        return tokens

class chatbot:
    def __init__(self, model,  max_seq_len, tokenizer, chat_format, generate_full_logit, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.chat_formatter = chat_format
        self.system_prompt = None
        self.max_seq_len = max_seq_len
        self.get_user_input: Callable = input
        self.generate_full_logit = generate_full_logit
        self.temperature = 0.0 
        self.top_k = 0

        self.eot_id = self.tokenizer.special_tokens["<|eot_id|>"]
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
        