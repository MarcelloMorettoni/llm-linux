import streamlit as st
import llm_utils
import command_utils
import config

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="OS Commander AI", layout="wide")

st.title("🤖 OS Commander AI")
st.caption("Enter a natural language command for your OS. The AI will suggest a shell command.")

# --- Initialize Session State ---
if 'suggested_command' not in st.session_state:
    st.session_state.suggested_command = None
if 'command_to_run' not in st.session_state:
    st.session_state.command_to_run = None
if 'command_output' not in st.session_state:
    st.session_state.command_output = None
if 'command_error' not in st.session_state:
    st.session_state.command_error = None
if 'user_query_history' not in st.session_state:
    st.session_state.user_query_history = []

# --- Helper Functions ---
def reset_state():
    st.session_state.suggested_command = None
    st.session_state.command_to_run = None
    st.session_state.command_output = None
    st.session_state.command_error = None

# --- Main Application Logic ---
with st.form("query_form"):
    natural_language_query = st.text_input(
        "What would you like to do?",
        placeholder="e.g., 'How many files are in my temp folder?' or 'Show current directory'",
        key="user_query_input"
    )
    submit_button = st.form_submit_button("✨ Get Command Suggestion")

if submit_button and natural_language_query:
    reset_state() # Reset previous state on new submission
    st.session_state.user_query_history.append(natural_language_query)
    with st.spinner("🧠 Thinking... Asking the AI for a command..."):
        suggested_cmd = llm_utils.get_command_from_llm(natural_language_query)
        if suggested_cmd:
            st.session_state.suggested_command = suggested_cmd
            st.session_state.command_to_run = suggested_cmd # Store for potential execution
        else:
            st.error("Could not get a command suggestion from the AI.")
            st.session_state.suggested_command = None # Ensure it's cleared

# --- Display Suggested Command and Confirmation ---
if st.session_state.suggested_command:
    st.subheader("💡 Suggested Command:")
    st.code(st.session_state.suggested_command, language="bash")

    st.warning("""
    **⚠️ Security Warning!**
    Review the command carefully before running. Executing unknown commands can be harmful.
    This tool is for demonstration and learning. Use with extreme caution.
    """)

    col1, col2, col3 = st.columns([1,1,5]) # Adjust column ratios as needed
    with col1:
        if st.button("✅ Yes, Run it!", key="run_button"):
            if st.session_state.command_to_run:
                is_valid, validation_message_or_command = command_utils.validate_command(
                    st.session_state.command_to_run,
                    config.ALLOWED_COMMANDS
                )
                if is_valid:
                    st.info(f"🚀 Executing: `{validation_message_or_command}`") # validation_message_or_command is the command string if valid
                    with st.spinner("⚙️ Running command..."):
                        output, error = command_utils.execute_command(validation_message_or_command)
                        st.session_state.command_output = output
                        st.session_state.command_error = error
                else:
                    st.error(f"🚫 Command Validation Failed: {validation_message_or_command}")
                    st.session_state.command_output = None
                    st.session_state.command_error = validation_message_or_command # Show validation error
            else:
                st.error("No command to run. Please get a suggestion first.")
    with col2:
        if st.button("❌ No, Cancel", key="cancel_button"):
            st.info("Command execution cancelled.")
            # Optionally clear the suggestion or allow editing
            reset_state()
            st.rerun() # Rerun to clear the suggested command from display immediately


# --- Display Command Output/Error ---
if st.session_state.command_output is not None:
    st.subheader("🖥️ Command Output:")
    st.text_area("Output", st.session_state.command_output, height=200, disabled=True)

if st.session_state.command_error:
    st.subheader("🔥 Command Error:")
    st.error(st.session_state.command_error)


# --- Display History (Optional) ---
# with st.expander("📜 Query History"):
#     if st.session_state.user_query_history:
#         for i, query in enumerate(reversed(st.session_state.user_query_history)):
#             st.write(f"{len(st.session_state.user_query_history) - i}. {query}")
#     else:
#         st.write("No queries yet.")

st.sidebar.header("About")
st.sidebar.info(
    "This is a Streamlit application that uses an LLM to suggest OS commands "
    "based on natural language input. "
    "It includes a crucial user confirmation step before any command execution."
)
st.sidebar.warning(
    "**Disclaimer:** This is a proof-of-concept and should be used with extreme caution. "
    "Always review commands before execution. The developers are not responsible for any "
    "damage caused by misuse of this tool."
)
st.sidebar.header("Configuration")
st.sidebar.caption("Allowed Commands (from config.py):")
for cmd in config.ALLOWED_COMMANDS:
    st.sidebar.markdown(f"- `{cmd}`")

if config.LLM_API_KEY == "YOUR_LLM_API_KEY_HERE":
    st.sidebar.error("LLM API Key not configured in `config.py`! The app will use placeholder LLM responses.")
else:
    st.sidebar.success("LLM API Key seems to be configured.")

