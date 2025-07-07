import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if not path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        elif not os.path.exists(file_path):
            return f'Error: File "{file_path}" not found.'
        elif path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python3", path],
                capture_output=True,
                timeout=30,
                cwd=working_directory,
                encoding='utf-8'
            )
        except Exception as e:
            return f"Error: executing Python file: {e}"

        output = ""
        if result.stdout != "" and result.stdout != None:
            output = f'STDOUT: {result.stdout}'

        if result.stderr != "" and result.stderr != None:
            if output != "":
                output += '\n'
            output += f'STDERR: {result.stderr}'

        if result.returncode != 0:
            if output != "":
                output += '\n'
            output += 'Process exited with code {result.returncode}'

        if output == "":
            output = "No output produced."
        return output

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory. Returns the contents of stdout, stderr, and the exit code, if they are not 0 or empty",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to execute, relative to the working directory. If not provided, or if file does not end in '.py' an error is returned.",
            ),
        },
    ),
)
