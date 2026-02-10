import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_functions import available_functions, function_call
from prompts import system_prompt
from config import AI_AGENT_MAX_LOOPS, AI_MODEL

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise Exception("no api key")

client = genai.Client(api_key=api_key)


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

if args.verbose:
    print(f"User prompt: {args.user_prompt}")

messages = [types.Content(role="user", parts = [types.Part(text=args.user_prompt)])]


for i in range(AI_AGENT_MAX_LOOPS):
    response = client.models.generate_content(
        model=AI_MODEL, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt, 
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)


    usage_stats = response.usage_metadata
    if usage_stats is not None:
        prompt_tokens = usage_stats.prompt_token_count
        response_tokens = usage_stats.candidates_token_count
        if args.verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        print("No usage metadata on this response.")

    candidate = []
    if response.function_calls:
        for func_call in response.function_calls:
            if not func_call:
                continue

            function_call_result = function_call(func_call, args.verbose) 
            if not function_call_result.parts:
                raise ValueError("function call result: missing parts")
            if not function_call_result.parts[0].function_response:
                raise ValueError("function call result: missing function response")
            if not function_call_result.parts[0].function_response.response:
                raise ValueError("function call result: missing function response response")
            candidate.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response['result']}")
        messages.append(types.Content(role="user", parts=candidate))
        if i == AI_AGENT_MAX_LOOPS:
            print(f'Error: Reached max iterations without answer. Exiting.')
            sys.exit(1)
    else:
        print("Response:")
        print(response.text)
        break

