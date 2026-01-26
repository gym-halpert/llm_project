import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot wirte to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing file contents: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified string content to a file located at a specific path relative to the specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path pointing to the file where the content is to be written (relative to the working directory)"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string value of the content to be written to the file",
            ),
        },
    ),
)
