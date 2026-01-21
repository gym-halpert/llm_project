import os
import sys
import argparse
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
    try:
        api_key
    except NameError:
        raise RuntimeError("API key not found...")
        sys.exit(1)

    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
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
        print(response.text)
    else:
        print(f"\nUser prompt: {args.user_prompt}")
        print(f"\n{response.text}\n")


if __name__ == "__main__":
    main()
