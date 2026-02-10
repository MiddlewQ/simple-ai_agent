import os, subprocess
from google.genai import types

from config import TIMEOUT_SECONDS

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file through the use of a subprocess. Return output from stdout and stderr or error message if unsuccessful.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the correct python script you want to run, relatively from the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments that can be passed to the python file. "
            )
        },
        required=["file_path"]
    )
)



def run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = os.path.commonpath([file_path_abs, working_directory_abs]) == working_directory_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python3", file_path_abs]
    if args:
        command.extend(args)

    try:
        result = subprocess.run(args=command,
                       cwd=working_directory_abs,
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       text=True,
                       timeout=TIMEOUT_SECONDS)
        output = []
        if result.returncode:
            output.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            output.append('No output produced')
        else:
            if result.stdout:
                output.append(f'STDOUT: {result.stdout}')
            if result.stderr:
                output.append(f'STDERR: {result.stderr}')
        
        return "\n".join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'
