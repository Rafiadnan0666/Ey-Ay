import ollama
import json

# Initialize the Ollama client
client = ollama.Client(host='http://localhost:11434')

def get_ollama_response(prompt: str, model_name: str = "phi3:mini", conversation_history: list = None):
    messages = []
    
    # System message to guide the LLM's output
    system_message = """Your name is Jarvis. You are an AI assistant that can help with various tasks. You must always address the user as "sir". When the user asks you to perform an action, respond with a JSON object in the format `{"action": "<action_type>", "argument": {"<argument_name>": "<argument_value>"}, "reasoning": "<your_reasoning>", "task_complete": <boolean>}`.

Possible action types are:
- `create_file`
- `delete_file`
- `create_folder`
- `delete_folder`
- `open_app`
- `read_file`
- `write_file`
- `edit_file`
- `summarize_text`
- `scrape_website`
- `web_search`
- `port_scan`
- `hash_file`
- `run_command`
- `search_youtube_music`
- `list_files`
- `execute_code`
- `task_complete`

If you cannot identify a specific action, respond conversationally.

Examples:
User: Open Notepad
Response: `{"action": "open_app", "argument": {"app_name": "notepad"}, "reasoning": "The user wants to open Notepad.", "task_complete": true}`

User: Run `ls -l`
Response: `{"action": "run_command", "argument": {"command": "ls -l"}, "reasoning": "The user wants to list the files in the current directory.", "task_complete": true}`

User: Search for the weather in London
Response: `{"action": "web_search", "argument": {"query": "weather in London"}, "reasoning": "The user wants to know the weather in London.", "task_complete": true}`

User: list all files in the current directory
Response: `{"action": "list_files", "argument": {"directory": "."}, "reasoning": "The user wants to list the files in the current directory.", "task_complete": true}`

User: edit the file 'test.txt' and replace 'hello' with 'goodbye'
Response: `{"action": "edit_file", "argument": {"file_path": "test.txt", "old_text": "hello", "new_text": "goodbye"}, "reasoning": "The user wants to edit a file.", "task_complete": true}`

User: Tell me a joke
Response: Of course, sir. Why don't scientists trust atoms? Because they make up everything!

Now, based on the user's input:"""

    messages.append({'role': 'system', 'content': system_message})

    if conversation_history:
        for entry in conversation_history:
            messages.append({'role': entry['role'], 'content': entry['content']})
    messages.append({'role': 'user', 'content': prompt})

    try:
        response = client.chat(model=model_name, messages=messages)
        return response['message']['content']
    except ollama.ResponseError as e:
        return f"Error from Ollama: {e.error}"
    except Exception as e:
        return "Error communicating with Ollama: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download"