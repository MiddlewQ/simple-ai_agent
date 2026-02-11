# AI Agent for File System Interaction

This project implements an AI agent that leverages the Gemini API to interact with the file system. The agent can perform various operations such as listing files, reading file contents, executing Python scripts, and writing to files.

This README.md file was created by the AI in the project.

## Features:

-   **File System Interaction**: The agent can perform the following actions:
    -   List files and directories within a specified path.
    -   Read the content of files (up to a maximum size, configurable in `agent/config.py`).
    -   Execute Python files with optional arguments.
    -   Write content to specified files, creating directories if they don't exist.
-   **Configurable AI Model**: The agent uses the `gemini-2.5-flash` model as default, which can be configured in the `agent/config.py` file.
-   **Loop Limit**: The AI agent has a configurable maximum number of interaction loops (`AI_AGENT_MAX_LOOPS`) to prevent infinite execution, defined in `agent/config.py`.
-   **API Key Management**: The Gemini API key is loaded from an `.env` file, ensuring secure handling of credentials.
-   **Sandboxed Workspace**: The agent is restricted to operate within the current working directory (`./sandbox`), as configured by `AI_WORKING_DIRECTORY` in `agent/config.py`.

## How it Works:

The `agent/cli.py` script serves as the command-line entry point, taking a user prompt as an argument. It then calls `run_agent` from `agent/runner.py`. The `agent/runner.py` script initializes the Gemini client and enters a loop where it sends the user's prompt and subsequent tool outputs to the AI model. The AI model, guided by a system prompt (defined in `agent/prompts.py`) and available function declarations, decides which file system operations to perform.

The `agent/tool_registry.py` file defines the available functions for the AI agent and maps them to their respective Python implementations, which are located in the `agent/tools/` directory. These functions are exposed to the Gemini model as `Tool` declarations.

## Setup:

1.  **Environment Variables**: Create a `.env` file in the project root and add your Gemini API key:

    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```

2.  **Dependencies**: Dependencies are defined in `pyproject.toml` and locked in `uv.lock`. Install them with:

    ```bash
    uv sync
    ```

    Notes:
    -   `uv sync` typically creates a local virtual environment (often `.venv/`), which is intentionally not committed to git.

## Usage:

Run the `agent/cli.py` script with a user prompt:

```bash
uv run python -m agent.main "Your prompt here" [--verbose]
```

-   `"Your prompt here"`: The task or question you want the AI agent to address.
-   `--verbose`: (Optional) Enables verbose output, showing prompt and response token counts, and the full function calls made by the agent.

## Project Structure:

-   `agent/`: The core directory for the AI agent.
    -   `cli.py`: The command-line interface for the AI agent.
    -   `runner.py`: Orchestrates the AI agent's interaction loop and Gemini client.
    -   `tool_registry.py`: Defines and maps the callable functions for file system interaction.
    -   `config.py`: Contains configuration settings for the AI agent.
    -   `tools/`: Contains individual modules for file system operations (e.g., `fs_read.py`, `fs_list.py`, `py_run.py`, `fs_write.py`).
    -   `prompts.py`: Contains the `system_prompt` used to guide the AI model.
-   `.env`: Stores environment variables, including the Gemini API key.
-   `pyproject.toml`: Defines project metadata and dependencies.
-   `uv.lock`: Locks the exact versions of project dependencies.
-   `README.md`: This file, providing an overview of the project.
-   `.gitignore`: Specifies intentionally untracked files to ignore.
-   `.python-version`: Specifies the Python version used.
-   `tests/`: Contains project tests.
-   `sandbox/`: A directory that might be used for testing or temporary files during development.

