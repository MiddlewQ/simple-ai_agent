import argparse

from .runner import run_agent

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    result = run_agent(args.user_prompt, verbose=args.verbose)
    print("Response")
    print(result.text)
    print_stats(result)

def print_stats(result):
    print("Stats:")
    print(f"Prompt Tokens: {result.prompt_tokens}")
    print(f"Response Tokens: {result.response_tokens}")