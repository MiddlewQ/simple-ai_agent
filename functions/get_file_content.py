import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of a file, provided filepath and directory status. Max size 10 000 characters. Display working directory as 'directory'",
    parameters=types.Schema(
        type=types.Type.STRING,
        description="File path to file to return content from, relatively from the working directory"
    )
)

def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = os.path.commonpath([target_file, working_directory_abs]) == working_directory_abs
    if not valid_target_file:
        return f'Error: Cannot retrieve content of "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(target_file, mode='r') as f:
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'...File "{file_path}" truncated at {MAX_CHARS}'
    
    return content