import os
import subprocess
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

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
    """Opens the specified application."""
    try:
        # For Windows
        if os.name == 'nt':
            os.startfile(app_name)
            return f"Opening {app_name}"
        # For macOS
        elif os.name == 'posix':
            subprocess.call(['open', '-a', app_name])
            return f"Opening {app_name}"
        else:
            return "Unsupported operating system."
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