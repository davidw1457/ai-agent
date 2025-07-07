import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from constants import SYSTEM_PROMPT, ITERATIONS, MODEL_NAME

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

    iteration = 0
    while 1 == 1:
        iteration += 1
        if iteration > ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)
            if response:
                print(response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    function_returns = []
    if not response.function_calls is None:
        for fc in response.function_calls:
            function_return = call_function(fc, verbose)
            if not function_return.parts or not function_return.parts[0].function_response.response:
                raise Exception(f"Error calling {fc.name} with {fc.args}")
            if verbose:
                print(f"-> {function_return.parts[0].function_response.response}")
            function_returns.append(function_return.parts[0])
    else:
        return response.text

    messages.append(types.Content(role="tool", parts=function_returns))

if __name__ == "__main__":
    main()
