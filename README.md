# AI-Powered Terminal Assistant (Jarvis)

This project provides an AI-powered terminal assistant named Jarvis that can understand natural language commands to perform various system operations, web searches, and application launches.

## Features

- **Voice Control:** Interact with Jarvis using voice commands.
- **File Operations:** Create, delete, read, write, and edit files and folders.
- **Application Launcher:** Open applications by their name.
- **Web Search:** Perform web searches and get results directly in the terminal.
- **Command Execution:** Run shell commands.
- **Port Scanning:** Perform basic network port scans.
- **File Hashing:** Calculate SHA-256 hashes of files.
- **YouTube Music Search:** Search for music on YouTube.
- **AI Integration (Ollama):** Leverage a local LLM (Ollama) to interpret complex natural language requests for the above actions.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ollama Setup:**
    -   Download and install Ollama from [ollama.ai](https://ollama.ai/).
    -   Pull the `qwen2.5:0.5b` model (or your preferred model):
        ```bash
        ollama pull qwen2.5:0.5b
        ```

3.  **Configuration (Optional):**
    -   The `config.json` file (if present) was previously used for application paths. The system now attempts to open applications by name directly using `subprocess.Popen`.

## Usage

To start Jarvis, run:

```bash
python main.py
```

Once Jarvis is listening, you can issue commands like:

-   "Hello Jarvis"
-   "Open Notepad"
-   "Run `dir`"
-   "Search for the current weather"
-   "Create file `my_document.txt`"
-   "Read file `important_notes.txt`"
-   "Exit"

## Project Structure

-   `main.py`: Main entry point, handles voice input/output and command dispatch.
-   `actions.py`: Contains functions for various system operations (file, app, web, etc.).
-   `ollama_integration.py`: Handles communication with the Ollama LLM for AI interpretation.
-   `requirements.txt`: Lists Python dependencies.
-   `config.json`: (Optional) Previously used for app paths, now less critical due to direct app launching.
