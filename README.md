# AI Agent for File System Interaction

This project implements an AI agent that leverages the Gemini API to interact with the file system. The agent can perform various operations such as listing files, reading file contents, executing Python scripts, and writing to files.

This README.md file was written by the AI.

## Features:

- **File System Interaction**: The agent can perform the following actions:
    - List files and directories within a specified path.
    - Read the content of files (up to a maximum size).
    - Execute Python files with optional arguments.
    - Write content to specified files, creating directories if they don't exist.
- **Configurable AI Model**: The agent uses the `gemini-2.5-flash` model, which can be configured.
- **Loop Limit**: The AI agent has a configurable maximum number of interaction loops (`AI_AGENT_MAX_LOOPS`) to prevent infinite execution.
- **API Key Management**: The Gemini API key is loaded from an `.env` file, ensuring secure handling of credentials.

## How it Works:

The `main.py` script serves as the entry point, taking a user prompt as an argument. It initializes the Gemini client and enters a loop where it sends the user's prompt and subsequent tool outputs to the AI model. The AI model, guided by a system prompt and available function declarations, decides which file system operations to perform.

The `call_functions.py` file defines the available functions for the AI agent and maps them to their respective Python implementations. These functions are exposed to the Gemini model as `Tool` declarations.

## Setup:

1.  **Environment Variables**: Create a `.env` file in the project root and add your Gemini API key:
    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```
2.  **Dependencies**: (Presumably, dependencies like `google-generativeai` and `python-dotenv` would be installed, though not explicitly shown in the provided files).

## Usage:

Run the `main.py` script with a user prompt:

```bash
python main.py "Your prompt here" [--verbose]
```

-   `"Your prompt here"`: The task or question you want the AI agent to address.
-   `--verbose`: (Optional) Enables verbose output, showing prompt and response token counts, and the full function calls made by the agent.

## Project Structure:

-   `main.py`: The main script that orchestrates the AI agent's interaction.
-   `call_functions.py`: Defines and maps the callable functions for file system interaction.
-   `config.py`: Contains configuration settings such as `AI_AGENT_MAX_LOOPS` and `AI_MODEL`.
-   `functions/`: (Implicitly contains modules for file system operations like `get_files_info`, `get_file_content`, `run_python_file`, `write_file`).
-   `prompts.py`: (Implicitly contains the `system_prompt` used to guide the AI model).
-   `calculator`: This is a dummy project the ai is currently allowed to operate in. The ai cannot affects files that is not below this directory, and the specified directory is currently managed through the config.py
