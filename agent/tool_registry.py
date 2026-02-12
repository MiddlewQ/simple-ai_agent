from google.genai import types

from .config import AI_WORKING_DIRECTORY
from .tools.fs_list import *
from .tools.fs_read import *
from .tools.py_run import *
from .tools.fs_write import *

available_functions = types.Tool(
    function_declarations=[schema_fs_list, schema_fs_read, schema_py_run, schema_fs_write]
)

def function_call(function_call, verbose=False):
    if verbose:
        print(f'Calling function: {function_call.name}({function_call.args})')
    else:
        print(f' - Calling function: {function_call.name}')

    tool_map = {
        "get_file_content": fs_read,
        "get_files_info": fs_list,
        "run_python_file": py_run,
        "write_file": fs_write,
    }
    
    tool_name = function_call.name or ""
    if tool_name not in tool_map:
        tool_response = {
            "ok": False,
            "error": {
                "type": "UnknownFunction",
                "message": f"Unknown function: {tool_name}"
            }
        }
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=tool_name,
                    response=tool_response
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args['working_directory'] = AI_WORKING_DIRECTORY

    tool_response = tool_map[tool_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=tool_name,
                response=tool_response,
            )
        ],
    )