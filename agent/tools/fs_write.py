import os
from google.genai import types

from .response_helper import *

schema_fs_write = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write content to a file within the working directory. Creates parent directories if needed. "
        "Overwrites the file. "
        "Returns JSON: {ok: bool, result?: string, meta?: {...}, error?: {type, message}}. "
        "file_path must be relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def fs_write(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    if os.path.commonpath([target_file, working_directory_abs]) != working_directory_abs:
        return response_error(
            error_type="PathOutsideWorkingDirectory",
            message=f'Cannot write to "{file_path}" because it is outside the permitted working directory',
        )
    if os.path.isdir(target_file):
        return response_error(
            error_type="IsADirectory",
            message=f'Cannot write to "{file_path}" because it is a directory',
        )

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, mode="w") as f:
            f.write(content)
            f.close()
        return response_ok(
            result=f'Successfully wrote to "{file_path}"',
            characters_written=len(content)
        )
    except OSError as e:
        return response_error(
            error_type="OSError",
            message=f'Failed to write to "{file_path}": {e}',
        )