import os
from google.genai import types
from .response_helper import *

schema_fs_list = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "List files in a directory within the working directory. "
        "Returns JSON: {ok: bool, result?: ..., meta?: {...}, error?: {type, message}}. "
        "Use directory='.' for the working directory. directory must be relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to list, relative to the working directory. Use '.' for the root.",
            ),
        },
        required=["directory"],
    ),
)


def fs_list(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    if os.path.commonpath([target_dir, working_directory_abs]) != working_directory_abs:
        return response_error(
            error_type="OutsideWorkingDirectory",
            message=f'Cannot list "{directory}" as it is outside the permitted working directory'
        )
    if not os.path.isdir(target_dir):
        return response_error(
            error_type="NotADirectory",
            message=f'"Cannot list files in "{directory}" as it is not a directory'
        )
    objects = []
    try:
        with os.scandir(target_dir) as it:
            for entry in it:
                is_dir = entry.is_dir(follow_symlinks=False)
                size = None
                if not is_dir:
                    size = entry.stat(follow_symlinks=False).st_size
                objects.append({
                    "name": entry.name, 
                    "size": size,
                    "is_dir": is_dir
                }) 
    except OSError as e:
        return response_error(
            error_type="OSError",
            message=f'Failed to read directory "{directory}": {e}',
        )

    return response_ok(
        result=objects,
        file_count=len(objects)
    )

