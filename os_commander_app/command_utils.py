import subprocess
import shlex
from typing import Tuple, List
import config

def validate_command(command_string: str, allowed_commands: List[str]) -> Tuple[bool, str]:
    """
    Validates if the command is allowed and basic sanitization.
    Returns a tuple: (is_valid, message_or_command_parts).
    If valid, message_or_command_parts is a list of command parts.
    If invalid, message_or_command_parts is an error message string.
    """
    if not command_string.strip():
        return False, "Command string cannot be empty."

    try:
        # Split the command string into parts. shlex handles spaces and quotes.
        parts = shlex.split(command_string)
    except ValueError as e:
        return False, f"Error parsing command: {e}. Ensure quotes are balanced."

    if not parts:
        return False, "Command string resulted in no executable parts."

    # The main command is the first part
    main_command = parts[0]

    # Check if the main command is in the allowed list
    # This is a basic check. More sophisticated checks might involve
    # analyzing arguments, especially for commands like 'find' or 'grep'.
    if main_command not in allowed_commands:
        # Allow pipelined commands if all individual commands are allowed
        if "|" in command_string:
            # This is a simplistic check for pipelines.
            # A more robust solution would parse the pipeline structure.
            individual_commands = command_string.split("|")
            for cmd_segment in individual_commands:
                segment_parts = shlex.split(cmd_segment.strip())
                if not segment_parts or segment_parts[0] not in allowed_commands:
                    return False, f"Command '{segment_parts[0] if segment_parts else cmd_segment.strip()}' in pipeline is not allowed."
            # If all parts of the pipeline are allowed, consider the command valid for now.
            # The execution part will handle the full pipeline.
            return True, command_string # Return the full string for pipeline execution
        else:
            return False, f"Command '{main_command}' is not in the allowed list: {allowed_commands}"

    # Basic argument validation (example: prevent path traversal)
    for part in parts[1:]: # Check arguments
        if ".." in part or part.startswith("/") and main_command not in ["ls", "cat", "head", "tail", "wc", "df"]: # Allow absolute paths for specific commands
             # This is a very naive check. Proper path sanitization is complex.
            if not (part.startswith("/tmp") and main_command in ["ls", "wc"]): # Allow /tmp for ls and wc
                 return False, f"Argument '{part}' contains potentially unsafe characters or paths."

    # If valid, return the original command string, as execute_command will use shell=True for pipelines
    # or shlex.split for single commands.
    return True, command_string


def execute_command(command_string: str) -> Tuple[str | None, str | None]:
    """
    Executes the shell command and returns its stdout and stderr.
    Uses shell=True for simplicity with pipelines, which requires caution.
    For single commands without pipes, shell=False is safer.
    """
    print(f"Executing command: {command_string}")
    try:
        # For commands involving pipes, shell=True is often necessary.
        # This has security implications if command_string is not thoroughly vetted.
        # Our validate_command is the first line of defense.
        if "|" in command_string:
            process = subprocess.Popen(
                command_string,
                shell=True, # Be cautious with shell=True
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                executable='/bin/bash' # Or your preferred shell
            )
        else:
            # For single commands, better to use shell=False
            cmd_parts = shlex.split(command_string)
            process = subprocess.Popen(
                cmd_parts,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        stdout, stderr = process.communicate(timeout=15) # Add a timeout

        if process.returncode != 0:
            # Prefer stderr if it has content, otherwise combine with stdout for error context
            error_message = stderr.strip() if stderr.strip() else f"Command failed with exit code {process.returncode}. Output: {stdout.strip()}"
            return None, error_message
        return stdout.strip(), stderr.strip() if stderr.strip() else None

    except subprocess.TimeoutExpired:
        return None, "Command execution timed out."
    except FileNotFoundError:
        # This can happen if the command itself (e.g., 'nonexistent_command') is not found
        return None, f"Error: The command '{shlex.split(command_string)[0]}' was not found. Ensure it is installed and in your PATH."
    except Exception as e:
        return None, f"An unexpected error occurred during command execution: {e}"

if __name__ == '__main__':
    # Test validation
    allowed = config.ALLOWED_COMMANDS
    valid_cmd_str = "ls -la /tmp"
    is_valid, msg_or_parts = validate_command(valid_cmd_str, allowed)
    print(f"Command: '{valid_cmd_str}', Valid: {is_valid}, Message/Parts: {msg_or_parts}")
    if is_valid:
        out, err = execute_command(msg_or_parts) # msg_or_parts is command_string if valid
        print(f"Output:\n{out}")
        if err: print(f"Error:\n{err}")

    invalid_cmd_str = "rm -rf /"
    is_valid, msg_or_parts = validate_command(invalid_cmd_str, allowed)
    print(f"Command: '{invalid_cmd_str}', Valid: {is_valid}, Message/Parts: {msg_or_parts}")

    pipelined_cmd_str = "ls -la /tmp | wc -l"
    is_valid, msg_or_parts = validate_command(pipelined_cmd_str, allowed)
    print(f"Command: '{pipelined_cmd_str}', Valid: {is_valid}, Message/Parts: {msg_or_parts}")
    if is_valid:
        out, err = execute_command(msg_or_parts)
        print(f"Output:\n{out}")
        if err: print(f"Error:\n{err}")

    disallowed_pipeline_cmd_str = "ls /tmp | sudo reboot"
    is_valid, msg_or_parts = validate_command(disallowed_pipeline_cmd_str, allowed)
    print(f"Command: '{disallowed_pipeline_cmd_str}', Valid: {is_valid}, Message/Parts: {msg_or_parts}")

