import os
import sys
import argparse
from prompts import system_prompt
from call_function import available_functions
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    try:
        response.usage_metadata
    except ValueError:
        raise RuntimeError("No metadata found...")
        sys.exit(1)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"\nUser prompt: {args.user_prompt}")
        print(f"\nPrompt tokens: {prompt_tokens}")
        print(f"\nResponse tokens: {response_tokens}\n")

    if not response.function_calls:
        print(f"Response: {response.text}")
        return

    for function_call in response.function_calls:
        print(f'Calling function: {function_call.name}({function_call.args})')
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
