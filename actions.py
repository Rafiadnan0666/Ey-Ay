import os
import subprocess
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nmap
import hashlib
from googlesearch import search
import ollama_integration

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

def summarize_text(text):
    """Summarizes the given text using sumy."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
    return " ".join(str(sentence) for sentence in summary)

def web_search(query):
    """Performs a web search using Google and returns the results."""
    try:
        results = []
        for j in search(query, num_results=3):
            results.append(j)
        return "\n".join(results) if results else "No results found."
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

def get_llm_response(prompt, conversation_history):
    return ollama_integration.get_ollama_response(prompt, conversation_history=conversation_history)