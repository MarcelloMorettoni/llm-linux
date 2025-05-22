# llinux - the llm-linux

OS Commander AI is a proof-of-concept web application that translates natural language into safe shell commands using an LLM (Large Language Model). Built with Streamlit, it allows users to query Linux/macOS system commands in plain English, review suggested shell commands, and execute them cautiously with built-in validation and security.

## Features

- Natural language to shell command translation via LLM
- Safe command validation before execution
- Secure subset of allowed commands
- Streamlit web UI for interaction and confirmation
- Command output and error display
- Support for pipelines if all commands are allowed

## Architecture Overview

- **Frontend:** Streamlit
- **Backend:** Python with optional LLM integration
- **Command Safety:** Validated against a whitelist (`ALLOWED_COMMANDS`)
- **Configuration:** Controlled through `config.py`

## Installation

1. Clone the repository.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your LLM API key and model in `config.py`:
   ```python
   LLM_API_KEY = "your_api_key"
   LLM_MODEL_NAME = "your_model"
   ```

## Usage

Run the app with Streamlit:
```bash
streamlit run app.py
```

Then open the local URL in your browser. Enter a natural language query like:

- "List all files in the temp directory"
- "What is the current directory?"
- "How many files are in /tmp?"

Review the suggested shell command and choose whether to run it.

## Configuration

I suggest you to use ollama:
```
pip install ollama
```
and then pull llama3, example:

```
ollama run llama3
```
However, it might work with another models.

Edit `config.py` to:

- Set your LLM API key and model
- Customize the allowed commands (`ALLOWED_COMMANDS`)
- Adjust the default prompt template if needed

## Security Notes

- Only read-only, non-destructive shell commands should be allowed.
- Commands are validated using `shlex.split` and a strict whitelist.
- Pipelines are allowed only if all subcommands are allowed.
- Placeholder logic is used if no API key is set.

## Example Allowed Commands

```python
ALLOWED_COMMANDS = [
    "ls", "pwd", "echo", "wc", "cat", "head", "tail", "df", "free", "uname", "date"
]
```

## Development Notes

- `llm_utils.py` handles LLM interaction (currently placeholder logic).
- `command_utils.py` validates and runs shell commands securely.
- `app.py` is the main UI entry point using Streamlit.

## Disclaimer

This tool is for educational and experimental purposes only. Always review commands before execution. The developers are not responsible for any misuse or damage caused.
