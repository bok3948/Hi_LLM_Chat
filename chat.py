import logging
from typing import  Dict, List, Optional,  Union, Tuple
from abc import ABC, abstractmethod
from typing import Callable

import torch

from tokenizer import Tokenizer

logger = logging.getLogger(__name__)

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

    @torch.no_grad()
    def generate(
        self,
        model,
        prompt: torch.Tensor,
        device: torch.device,
        *,
        start_pos: int = 0,
        callback=lambda x: x,
        ):
        """
        Takes a conditioning sequence (prompt) as input and continues to generate as many tokens as requested.
        """
        if len(prompt.shape) > 1:
            prompt = prompt.squeeze(0)
        prompt_length = prompt.size(0)

        max_new_tokens = self.max_seq_len - start_pos - prompt_length

        input_pos = torch.arange(
            start_pos, prompt_length + start_pos, device=device, dtype=torch.int
        )

        next_token = self.prefill(
            model,
            prompt.view(1, -1),
            input_pos,
        )

        callback(next_token.clone().view(-1))

        input_pos = torch.tensor(
            [start_pos + prompt_length], device=device, dtype=torch.int
        )

        generated_tokens = []
        for generated_token, _ in self.decode_n_tokens(
            model,
            next_token,
            input_pos,
            max_new_tokens - 1,
            callback=callback,
        ):
            generated_tokens.append(generated_token.view(-1))
            yield generated_token, None

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
    
    def decode_n_tokens(
        self,
        model,
        cur_token: torch.Tensor,
        input_pos: torch.Tensor,
        num_new_tokens: int,
        callback=lambda _: _,
    ):
        new_tokens = []
        encountered_eos = False
        for _i in range(
            num_new_tokens - 1
        ):  # -1 to save space to run an EoS if dont generate it naturally
            # Actually better for Inductor to codegen attention here

            out_token = cur_token.clone()
            next_token, next_prob = self.decode_one_token(
                model,
                out_token,
                input_pos,
            )
            input_pos += 1
            new_tokens.append(next_token.clone())
            callback(new_tokens[-1])

            yield out_token, None
            cur_token = next_token

            # encountered eos
            if next_token.item() == self.eot_id:
                encountered_eos = True
                final_token, next_prob = self.decode_one_token(
                    model,
                    cur_token,
                    input_pos,
                )
                input_pos += 1
                break

        if not encountered_eos:
            eos_token = torch.tensor(
                [self.eot_id],
                dtype=cur_token.dtype,
                device=cur_token.device,
            )
            new_tokens.append(eos_token.clone())
            eos_token, next_prob = self.decode_one_token(
                model,
                eos_token.view(1, -1),
                input_pos,
            )
            input_pos += 1
            yield eos_token.clone(), (
                 None
            )

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

            
        return idx_next, probs

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


    def chat(
        self,
    ):
        print("Starting Multi Turn Chat if you want to exit say /bye")

        start_pos = 0
        self.system_prompt = None


        get_system_prompt = self.get_user_input(
           "Do you want to enter a system prompt? Enter y for yes and anything else for no. \n"
        )
        if get_system_prompt == "y" or get_system_prompt == "Y":
           self.system_prompt = self.get_user_input("What is your system prompt? \n")

        for i in range(1000):
            is_first_sample: bool = i == 0
            print("\n")
            prompt = self.get_user_input("User: ")

            if prompt == "/bye":
                print("Exiting Chat.\n")
                break
            
            messages_to_encode = []
            if is_first_sample and self.system_prompt:
                messages_to_encode.append(
                    {"role": "system", "content": self.system_prompt}
                )
            messages_to_encode.append({"role": "user", "content": prompt})
            encoded = self.chat_formatter.encode_dialog_prompt(
                messages_to_encode, add_generation_prompt=True,
            )
            encoded = torch.tensor(
                encoded, dtype=torch.int, device=self.device
            )

            if encoded.size(0) + start_pos > self.max_seq_len:
                print(
                    "This prompt would take us past the max_seq_length. Ending Conversation."
                )
                break

            print("Model: ", end="")
            buffer = []

            def callback(x, *, done_generating=False):
                return self._callback(
                    x,
                    buffer=buffer,
                    done_generating=done_generating,
                )

            generator_func = self.generate(
                    model = self.model,
                    prompt=encoded,
                    device=self.device,
                    callback=callback,
                    start_pos=start_pos,
                )

            start_pos += encoded.size(0)

            for token_tensor, metrics in generator_func:
                if token_tensor is not None:
                    start_pos += token_tensor.size(0)

if __name__ == "__main__":
    model = torch.load("./model.pt", weights_only=False)
    tokenizer = Tokenizer("./tokenizer.model")
    chat_format = Llama3ChatFormatter(tokenizer)
    model = model.to("cuda")
    chat_bot = chatbot(model,  256, tokenizer, chat_format, device="cuda", generate_full_logit=True)
    chat_bot.chat()
