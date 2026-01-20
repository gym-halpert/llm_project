import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()


def main():
    try:
        api_key
    except NameError:
        raise RuntimeError("API key not found...")
        sys.exit(1)

    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
    )

    try:
        response.usage_metadata
    except ValueError:
        raise RuntimeError("No metadata found...")
        sys.exit(1)

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)

if __name__ == "__main__":
    main()
