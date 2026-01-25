import os

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside of the permitted working directory'
        if os.path.isdir(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        content = ""

        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters'

        return content

    except Exception as e:
        return f"Error listing file contents: {e}"
