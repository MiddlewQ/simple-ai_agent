import os
from agent.config import FILE_MAX_CHARS
from google.genai import types
from .response_helper import *

schema_fs_read = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read a text file within the working directory and return its content. "
        f"Reads up to {FILE_MAX_CHARS} characters; if truncated, meta.truncated=true. "
        "Returns JSON: {ok: bool, result?: string, meta?: {...}, error?: {type, message}}. "
        "file_path must be relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def fs_read(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = os.path.commonpath([target_file, working_directory_abs]) == working_directory_abs
    if not valid_target_file:
        return response_error(
            error_type="PathOutsideWorkingDirectory", 
            message= f'Cannot retrieve content of "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.isfile(target_file):
        return response_error(
            error_type="NotAFile",
            message=f'File not found or is not a regular file: "{file_path}"'
        )
    
    try:
        with open(target_file, mode='r') as f:
            content = f.read(FILE_MAX_CHARS)
            truncated = f.read(1) != ""
        meta = {
            "truncated": truncated,
            "max_chars": FILE_MAX_CHARS,
        }
        if truncated:
            meta['message'] = f'...File "{file_path}" truncated at {FILE_MAX_CHARS}'

        return response_ok(
            result=content,
            meta=meta
        )
    except OSError as e:
        return response_error(
            error_type="OSError",
            message=f'Failed to read "{file_path}": {e}'
        )