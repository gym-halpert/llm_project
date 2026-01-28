import os
import sys
import argparse
from prompts import system_prompt
from call_function import available_functions
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function

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

    for _ in range(20):

        response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

        for candidate in response.candidates:
            content = candidate.content
            messages.append(content)

        if not response.function_calls:
            print(f"Final Response: {response.text}")
            return

        func_results_list = []

        for function in response.function_calls:
            called = call_function(function, verbose=args.verbose)

            if len(called.parts) == 0:
                raise RuntimeError(f'Error: Parts list is empty')

            if not called.parts[0].function_response:
                raise RuntimeError(f'Error: Function response object is None')

            if not called.parts[0].function_response.response:
                raise RuntimeError(f'Error: Function response is None')

            func_results_list.append(called.parts[0])

            if args.verbose:
                print(f"-> {called.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=func_results_list))

    print("Max iterations reached")

if __name__ == "__main__":
    main()
