import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content input to the target file_path. Will create directories if they do not exist in the file path. File will be opened in write mode. Returns error or success message.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file you want to write to, relative from the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that should be written to file."
            )
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = os.path.commonpath([target_file, working_directory_abs]) == working_directory_abs
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    target_dir = os.path.dirname(target_file)
    os.makedirs(target_dir, exist_ok=True)


    with open(target_file, mode="w") as f:
        f.write(content)
        f.close()

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

