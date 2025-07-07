import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working direcctory iin your function calls as it is automatically injected for security reasons.
"""
model_name = "gemini-2.0-flash-001"

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    if len(sys.argv) < 2:
        print("no prompt provided")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {user_prompt}")
    response = generate_content(client, messages, verbose)
    print(response)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if not response.function_calls is None:
        for fc in response.function_calls:
            function_return = call_function(fc, verbose)
            if not function_return.parts[0].function_response.response:
                raise Exception(f"Error calling {fc.name} with {fc.args}")
            elif verbose:
                print(f"-> {function_return.parts[0].function_response.response}")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return response.text

if __name__ == "__main__":
    main()
