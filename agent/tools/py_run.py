import os, subprocess
from google.genai import types

from agent.config import TIMEOUT_SECONDS
from .response_helper import *

schema_py_run = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python script within the working directory using a subprocess. "
        "Returns JSON: {ok: bool, result?: {stdout: string, stderr: string}, meta?: {...}, error?: {type, message}}. "
        "Non-zero exit codes return ok=false with stdout/stderr included. "
        "file_path must be relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the .py file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)



def py_run(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.normpath(os.path.join(working_directory_abs, file_path)))
    if os.path.commonpath([file_path_abs, working_directory_abs]) != working_directory_abs:
        return response_error(
            error_type="PathOutsideWorkingDirectory",
            message=f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
    if not os.path.isfile(file_path_abs):
        return response_error(
            error_type="NotAFile",
            message=f'"{file_path}" does not exist or is not a regular file'
        )
        
    if not file_path_abs.endswith(".py"):
        return response_error(
            error_type="NotPythonFile",
            message=f'"{file_path}" is not a Python file',
        )
    
    command = ["python3", file_path_abs]
    if args:
        command.extend(args)

    try:
        process = subprocess.run(args=command,
                       cwd=working_directory_abs,
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       text=True,
                       timeout=TIMEOUT_SECONDS)
        result = {"stdout": process.stdout or "", "stderr": process.stderr or ""}
        output = []
        if process.returncode != 0:
            return response_error(
                error_type="ProcessExitNonZero",
                message=f"Process exited with code {process.returncode}",
                exit_code=process.returncode,
                command=command)
        
        return response_ok(
            result=result,
            exit_code=process.returncode, 
            command=command
        )
    except subprocess.TimeoutExpired as e:
        result = {"stdout": getattr(e, "stdout", "") or "", "stderr": getattr(e, "stderr", "") or ""}
        return response_error(error_type="Timeout",
                        message=f"Process exceeded timeout of {TIMEOUT_SECONDS} seconds",
                        result=result,
                        timeout_seconds=TIMEOUT_SECONDS,
                        command=command)
    except OSError as e:
        return response_error(
            error_type="OSError", 
            message=f"Failed to execute process: {e}", 
            command=command)