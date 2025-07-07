import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if not path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the specified file path, overwriting any current contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write the contents to, relative to the working directory. If not provided or unable to write to an error will be returned.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to write to the providded file path.",
            ),
        },
    ),
)
