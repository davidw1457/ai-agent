import os

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
