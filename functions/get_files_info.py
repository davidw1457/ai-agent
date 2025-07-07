import os
from google.genai import types

def get_files_info(working_directory, directory='.'):
    try:
        working_directory = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, directory))
        if not path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(path):
            return f'Error: "{directory} is not a directory'

        contents = os.listdir(path)
        contents_details = ""
        for item in contents:
            path = os.path.join(working_directory, directory, item)
            contents_details += f"\n- {item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}"

        return contents_details[1:]
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
