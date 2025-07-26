import ollama

def get_ollama_response(prompt: str, model_name: str = "qwen2.5:0.5b", conversation_history: list = None):
    messages = []
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