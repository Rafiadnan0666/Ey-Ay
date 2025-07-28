import ollama
import json

def get_ollama_response(prompt: str, model_name: str = "qwen2.5:0.5b", conversation_history: list = None):
    messages = []
    
    # System message to guide the LLM's output
    system_message = """Your name is Jarvis. You are an AI assistant that can help with various tasks. If the user asks you to open an application, run a command, or search the web, respond with a JSON object in the format `{"action": "<action_type>", "argument": "<argument_value>"}`. 
Possible action types are: `open_app`, `run_command`, `web_search`. 
If you cannot identify a specific action, respond conversationally.

Examples:
User: Open Notepad
Response: `{"action": "open_app", "argument": "notepad"}`

User: Run `ls -l`
Response: `{"action": "run_command", "argument": "ls -l"}`

User: Search for the weather in London
Response: `{"action": "web_search", "argument": "weather in London"}`

User: Tell me a joke
Response: Why don't scientists trust atoms? Because they make up everything!

Now, based on the user's input:"""

    messages.append({'role': 'system', 'content': system_message})

    if conversation_history:
        for entry in conversation_history:
            messages.append({'role': entry['role'], 'content': entry['content']})
    messages.append({'role': 'user', 'content': prompt})

    try:
        response = ollama.chat(model=model_name, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

if __name__ == "__main__":
    print("Testing Ollama integration...")
    test_prompt = "Hello, what is your purpose?"
    response = get_ollama_response(test_prompt)
    print(f"Prompt: {test_prompt}")
    print(f"Response: {response}")

    test_prompt_open_app = "Can you open Google Chrome?"
    response_open_app = get_ollama_response(test_prompt_open_app)
    print(f"Prompt: {test_prompt_open_app}")
    print(f"Response: {response_open_app}")

    test_prompt_run_command = "Execute the command `dir`"
    response_run_command = get_ollama_response(test_prompt_run_command)
    print(f"Prompt: {test_prompt_run_command}")
    print(f"Response: {response_run_command}")

    test_prompt_web_search = "Find information about the history of AI"
    response_web_search = get_ollama_response(test_prompt_web_search)
    print(f"Prompt: {test_prompt_web_search}")
    print(f"Response: {response_web_search}")