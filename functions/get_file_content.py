import os
from google.genai import types

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    working_directory = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(path, "r") as f:
            file_contents = f.read(MAX_CHARS+1)

        if len(file_contents) > MAX_CHARS:
            file_contents = f'{file_contents[:-1]}[...File "{file_path}" truncated at 10000 characters]'

        return file_contents
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first 10000 characters of the content from a sepcified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    )
)
