from .shell import main_loop
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="meta-llama/Llama-3.2-1B-Instruct", help="LLM to use")
    args = parser.parse_args()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main_loop(args.model)

if __name__ == "__main__":
    main()