import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

#    print(f"{working_dir_abs}\n{target_dir}\n{valid_target_dir}\n")

    dir_test = os.path.isdir(target_dir)
    listed_target = os.listdir(target_dir)

#    print(f"{dir_test}\n{listed_target}")

#    if not valid_target_dir:
#        print(f"Result for '{directory}' directory:")
#        raise ValueError(f'  Error: Cannot list "{directory}" as it is outside the permitted working directory')

#    if not dir_test:
#        print(f"Result for '{directory}' directory:")
#        raise TypeError(f'  Error: "{directory}" is not a directory')

#    try:
    for item in listed_target:

        if not valid_target_dir:
            print(f"Result for '{directory}' directory:")
            print(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return

        if not dir_test:
            print(f"Result for '{directory}' directory:")
            print(f'    Error: "{directory}" is not a directory')
            return

        if listed_target.index(item) == 0:
            print(f"Result for '{directory}' directory:")
        file_path = os.path.normpath(os.path.join(target_dir, item.strip("'")))
        size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
       	print(f"  - {item}: file_size={size} bytes, is_dir={is_dir}")

#    except ValueError as v:
#        return v
#    except TypeError as t:
#        return t
#    except Exception as e:
#        return f"  Error: An unexpected error has occurred: {e}"
