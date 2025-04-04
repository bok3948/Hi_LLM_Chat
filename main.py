import argparse
import os

from chat import Llama3ChatFormatter, chatbot
from tokenizer import Tokenizer
from models.llama_transformer import get_llama_3_2_instruct_1B


def get_args_parser():
    parser = argparse.ArgumentParser(description='Llama chatbot', add_help=False)

    parser.add_argument('--model_folder_path', type=str, default="./Llama3.2-1B-Instruct", help='Path to the main model parameter file')

    parser.add_argument('--use_kv_cache', action='store_true', default=True, help='Use KV cache for faster inference')

    parser.add_argument('--enable_dynamic_shape', action='store_true', default=False, help='Enable dynamic shape')

    parser.add_argument('--max_seq_len', type=int, default=1024, help='Maximum sequence length')

    parser.add_argument('--generate_full_logit', action='store_true', default=True, help='Generate full logits')

    parser.add_argument('--device', type=str, default='cuda', help='Device to run the model on (e.g., cuda, cpu)')

    return parser


def main(args):
    model = get_llama_3_2_instruct_1B(
            args.model_folder_path,
            use_kv_cache=args.use_kv_cache,
            enable_dynamic_shape=args.enable_dynamic_shape,
            max_seq_len=args.max_seq_len,
            max_batch_size=1,
            generate_full_logit=args.generate_full_logit,
        )
    tokenizer = Tokenizer(os.path.join(args.model_folder_path, 'tokenizer.model'))
    chat_format = Llama3ChatFormatter(tokenizer)
    model = model.to(args.device)
    chat_bot = chatbot(model, args.max_seq_len, tokenizer, chat_format, device=args.device, generate_full_logit=args.generate_full_logit)
    chat_bot.chat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('LLM chatbot', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)


