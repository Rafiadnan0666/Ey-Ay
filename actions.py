import os
import subprocess
import json
import sys
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nmap
import hashlib
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import ollama_integration
import asyncio

def create_file(file_path):
    """Creates an empty file at the specified path."""
    try:
        with open(file_path, 'w') as f:
            pass
        return f"File created: {file_path}"
    except Exception as e:
        return f"Error creating file: {e}"

def delete_file(file_path):
    """Deletes the specified file."""
    try:
        os.remove(file_path)
        return f"File deleted: {file_path}"
    except Exception as e:
        return f"Error deleting file: {e}"

def create_folder(folder_path):
    """Creates a new directory at the specified path."""
    try:
        os.makedirs(folder_path)
        return f"Folder created: {folder_path}"
    except Exception as e:
        return f"Error creating folder: {e}"

def delete_folder(folder_path):
    """Deletes the specified folder and all its contents."""
    try:
        os.rmdir(folder_path)
        return f"Folder deleted: {folder_path}"
    except Exception as e:
        return f"Error deleting folder: {e}"

def open_application(app_name):
    """Opens the specified application from the config file."""
    try:
        with open('config.json') as f:
            config = json.load(f)
            app_path = config['apps'].get(app_name.lower())

        if not app_path:
            return f"Application '{app_name}' not found in config.json."

        if os.name == 'nt':
            os.startfile(app_path)
        elif os.name == 'posix':
            subprocess.call(['open', '-a', app_path])
        else:
            return "Unsupported operating system."
        return f"Opening {app_name}"
    except Exception as e:
        return f"Error opening application: {e}"


def read_file_content(file_path):
    """Reads the content of the specified file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"

def write_file_content(file_path, content):
    """Writes content to the specified file. Creates the file if it doesn't exist."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Content written to {file_path}"
    except Exception as e:
        return f"Error writing to file: {e}"

def edit_file_content(file_path, old_text, new_text):
    """Replaces old_text with new_text in the specified file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        new_content = content.replace(old_text, new_text)
        with open(file_path, 'w') as f:
            f.write(new_content)
        return f"Content in {file_path} updated."
    except Exception as e:
        return f"Error editing file: {e}"

def summarize_text(text):
    """Summarizes the given text using sumy."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
    return " ".join(str(sentence) for sentence in summary)


def scrape_website(url):
    """Scrapes the text content of a website."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return f"Error scraping website: {e}"


from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def web_search(query):
    """Performs a web search, scrapes the top result, and returns a summary."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=1)]
            if not results:
                return "No results found."

            top_result_url = results[0]['href']
            
            # Scrape the website content
            scraped_text = scrape_website(top_result_url)
            if "Error" in scraped_text:
                return scraped_text

            # Summarize the content
            summary = summarize_text(scraped_text)
            return summary if summary else "Could not summarize the content."
    except Exception as e:
        return f"Error performing web search: {e}" 


def port_scan(target, ports):
    """Performs a port scan on the specified target."""
    try:
        nm = nmap.PortScanner()
        nm.scan(target, ports)
        return nm.csv()
    except Exception as e:
        return f"Error performing port scan: {e}"

def hash_file(file_path):
    """Calculates the SHA-256 hash of a file."""
    try:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error hashing file: {e}"

def run_command(command):
    """Executes a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error executing command: {e}"

def search_youtube_music(query):
    """Searches for music on YouTube."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.videos(f"{query} youtube music", max_results=3)]
            if not results:
                return "No music found on YouTube."
            
            links = [result['content'] for result in results]
            return "\n".join(links)

    except Exception as e:
        return f"Error searching YouTube music: {e}"

def get_llm_response(prompt, conversation_history):
    return ollama_integration.get_ollama_response(prompt, conversation_history=conversation_history)

def open_app_by_name(app_name):
    """Opens the specified application by name using subprocess.Popen."""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(app_name, shell=True)
        elif os.name == 'posix':  # macOS or Linux
            subprocess.Popen(['open', app_name])
        else:
            return "Unsupported operating system."
        return f"Opening {app_name}"
    except Exception as e:
        return f"Error opening application: {e}"

def list_files(directory="."):
    """Lists files in the specified directory."""
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

def execute_code(code):
    """Executes a string of Python code."""
    try:
        output = exec(code)
        return output
    except Exception as e:
        return f"Error executing code: {e}"

def task_complete(reasoning):
    """Signals that the task is complete."""
    return reasoning

async def do_until_done(prompt, conversation_history):
    """Executes a series of actions to complete a task."""
    while True:
        llm_response = await asyncio.to_thread(ollama_integration.get_ollama_response, prompt, conversation_history)
        try:
            parsed_response = json.loads(llm_response)
            action = parsed_response.get("action")
            arguments = parsed_response.get("argument")
            reasoning = parsed_response.get("reasoning")
            task_is_complete = parsed_response.get("task_complete")

            if task_is_complete:
                return reasoning

            if hasattr(sys.modules[__name__], action):
                action_func = getattr(sys.modules[__name__], action)
                if asyncio.iscoroutinefunction(action_func):
                    response = await action_func(**arguments)
                else:
                    response = await asyncio.to_thread(action_func, **arguments)
                
                print(response)
                conversation_history.append({'role': 'assistant', 'content': response})
                prompt = f"The last action returned: {response}. What is the next action?"
            else:
                return f"Unknown action: {action}"
        except json.JSONDecodeError:
            return llm_response

