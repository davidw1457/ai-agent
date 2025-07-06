import os

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
