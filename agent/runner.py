import os, sys
from dotenv import load_dotenv
from dataclasses import dataclass
from google import genai
from google.genai import types

from .config import AI_AGENT_MAX_LOOPS, AI_MODEL
from .tool_registry import available_functions, function_call
from .prompts import system_prompt

@dataclass
class RunResult:
    text: str
    prompt_tokens: int | None = None
    response_tokens: int | None = None

def _require_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY (set it in .env or env vars).")
    return api_key




def run_agent(prompt, verbose) -> RunResult:
    api_key = _require_api_key()
    client = genai.Client(api_key=api_key)
    
    messages = [types.Content(role="user", parts = [types.Part(text=prompt)])]

    total_prompt_tokens   = 0
    total_response_tokens = 0

    for step in range(AI_AGENT_MAX_LOOPS):
        response = client.models.generate_content(
            model=AI_MODEL, 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt, 
            ),
        )
        cand = response.candidates[0] if response.candidates else None
        if cand and cand.content:
            messages.append(cand.content)
        
        usage = response.usage_metadata
        if usage is not None:
            prompt_tokens = usage.prompt_token_count or 0
            response_tokens = usage.candidates_token_count or 0
            total_prompt_tokens += prompt_tokens
            total_response_tokens += response_tokens

            if verbose:
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")



        if response.function_calls:
            for fc in response.function_calls:
                if fc is None:
                    continue

                tool_content = function_call(fc, verbose)  # Content(role="tool", ...)
                messages.append(tool_content)

                if verbose:
                    if not tool_content.parts:
                        raise ValueError("Tool content has no parts")
                    part = tool_content.parts[0]
                    fr = part.function_response
                    if fr is None or fr.response is None or not isinstance(fr.response, dict):
                        raise ValueError("Tool content missing function_response.response dict")

                    r = fr.response
                    if r.get("ok") is True:
                        print(f"-> OK: {r.get('result')!r}")
                    else:
                        print(f"-> ERR: {r.get('error')!r}")
            continue

        
        return RunResult(
            text=response.text or "",
            prompt_tokens=total_prompt_tokens,
            response_tokens=total_response_tokens,
        )

    raise RuntimeError("Reached max iterations without producing final answer.")