# LLM Configuration (replace with your actual details)
LLM_API_KEY = "YOUR_LLM_API_KEY_HERE"
LLM_MODEL_NAME = "llama3" # Example, change to your model

# Security Configuration
# IMPORTANT: Start with a very restrictive list of commands.
# These are examples of relatively safe, read-only commands.
# Expand with extreme caution.
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "echo",
    "wc",    # word count
    "cat",   # display file content (be careful with large files)
    "head",  # display first few lines
    "tail",  # display last few lines
    "df",    # disk free
    "free",  # memory usage
    "uname", # system information
    "date",  # current date and time
    # "find", # powerful, but can be resource-intensive. Use with specific, safe patterns.
]

# You might want to add more specific configurations,
# e.g., for paths or LLM prompt templates
DEFAULT_PROMPT_TEMPLATE = """
You are an AI assistant that translates natural language requests from a user
into executable shell commands for a Linux/macOS environment.

The user's request is: "{user_query}"

Your task is to generate the most appropriate and direct shell command to fulfill this request.
Consider the context of common command-line operations.
Output *only* the shell command and nothing else.
For example:
User request: "What is the current directory?"
Shell command: pwd
User request: "List files in my documents folder."
Shell command: ls ~/Documents
User request: "How many lines are in the file 'report.txt'?"
Shell command: wc -l report.txt
"""
