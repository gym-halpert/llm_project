import os

def run_python_file(working_directory, file_path, args=None):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        completed = subprocess.run(commad, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abs_working_dir, timeout=30)
