import os

def get_files_info(working_directory, directory=None):
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
