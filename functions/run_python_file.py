import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        completed = subprocess.run(command, capture_output=True, text=True, cwd=abs_working_dir, timeout=30)
#        STDOUT = f'{completed.stdout.strip()}'
#        STDERR = f'{completed.stderr.strip()}'

        output = []

        if completed.returncode != 0:
            return f'Process completed with return code {completed.returncode}'

        if not completed.stdout and not completed.stderr:
            return f'No output produced'
        else:
            output.append(f'STDOUT: {completed.stdout.strip()}')
            output.append(f'STDERR: {completed.stderr.strip()}')
            output_string = "\n".join(output)
        return output_string

    except Exception as e:
        return f'Error executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Uses python and any additional arguments to run a .py file in a directory relative to the strict working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the .py file that will be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of strings that are passed as arguments to the script"
            ),
        },
    ),
)
