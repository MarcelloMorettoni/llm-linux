import os
import ollama
import config
# Import your chosen LLM library, e.g.:
# from openai import OpenAI
# import google.generativeai as genai

import config

# Placeholder for LLM client initialization
# client = None
# if config.LLM_API_KEY and config.LLM_API_KEY != "YOUR_LLM_API_KEY_HERE":
#     # Example for OpenAI:
#     # client = OpenAI(api_key=config.LLM_API_KEY)
#     # Example for Google Generative AI:
#     # genai.configure(api_key=config.LLM_API_KEY)
#     pass # Initialize your client here

def get_command_from_llm(natural_language_query: str) -> str | None:
    """
    Uses Ollama with LLaMA 3.3 to generate a shell command from natural language.
    """
    prompt = config.DEFAULT_PROMPT_TEMPLATE.format(user_query=natural_language_query)

    try:
        response = ollama.chat(
            model=config.LLM_MODEL_NAME,  # e.g. "llama3"
            messages=[
                {"role": "system", "content": "You are an AI assistant that translates natural language to shell commands."},
                {"role": "user", "content": prompt}
            ]
        )
        suggested_command = response['message']['content'].strip()
        return suggested_command

    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return None
        
    """
    Sends the natural language query to the LLM and returns the suggested shell command.
    """
    # global client
    if not config.LLM_API_KEY or config.LLM_API_KEY == "YOUR_LLM_API_KEY_HERE":
        print("LLM API Key not configured in config.py. Returning placeholder.")
        # For testing without an API key, you can return a fixed command
        # or a transformation of the input.
        if "list files" in natural_language_query.lower():
            if "tmp" in natural_language_query.lower():
                return "ls /tmp"
            return "ls"
        if "how many files" in natural_language_query.lower():
            if "tmp" in natural_language_query.lower():
                 return "ls /tmp | wc -l"
            return "ls | wc -l"
        if "current directory" in natural_language_query.lower():
            return "pwd"
        return f"echo 'LLM not configured to process: {natural_language_query}'"

    prompt = config.DEFAULT_PROMPT_TEMPLATE.format(user_query=natural_language_query)

    try:
        # --- LLM API Call ---
        # This is where you would integrate with your chosen LLM API.
        # Example for OpenAI (conceptual):
        # response = client.chat.completions.create(
        #     model=config.LLM_MODEL_NAME,
        #     messages=[
        #         {"role": "system", "content": "You are an AI assistant that translates natural language to shell commands."},
        #         {"role": "user", "content": prompt} # Or simplify prompt structure as needed
        #     ],
        #     temperature=0.2, # Lower temperature for more deterministic command generation
        #     max_tokens=50
        # )
        # suggested_command = response.choices[0].message.content.strip()
        # return suggested_command

        # Example for Google Generative AI (conceptual):
        # model = genai.GenerativeModel(config.LLM_MODEL_NAME)
        # response = model.generate_content(prompt)
        # suggested_command = response.text.strip()
        # return suggested_command

        # --- Placeholder until LLM is integrated ---
        print(f"Simulating LLM call for: {natural_language_query}")
        # This is a very basic placeholder, replace with actual LLM logic
        if "list files" in natural_language_query.lower():
            return "ls -la"
        elif "what is the current directory" in natural_language_query.lower():
            return "pwd"
        else:
            return f"echo 'Placeholder response for: {natural_language_query}'"
        # --- End Placeholder ---

    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

if __name__ == '__main__':
    # Test the function (optional)
    # Ensure you have your API key in config.py if you uncomment the actual LLM calls
    test_query = "list all files in the current directory with details"
    command = get_command_from_llm(test_query)
    if command:
        print(f"Natural Language Query: {test_query}")
        print(f"Suggested Command: {command}")
    else:
        print(f"Could not generate command for: {test_query}")

    test_query_2 = "how many files are in /tmp"
    command_2 = get_command_from_llm(test_query_2)
    if command_2:
        print(f"Natural Language Query: {test_query_2}")
        print(f"Suggested Command: {command_2}")

