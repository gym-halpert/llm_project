import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    dir_test = os.path.isdir(target_dir)
    listed_target = os.listdir(target_dir)

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if dir_test == False:
        return f'Error: "{directory}" is not a directory'

    for item in listed_target:
        size = os.path.getsize(item)
        file = os.path.isdir(item)
        return f"- {item}: file_size={size} bytes, is_dir={file}"
