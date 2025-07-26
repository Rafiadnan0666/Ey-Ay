import speech_recognition as sr
import pyttsx3
import actions
import ollama_integration
import json

# Global variable to store conversation history
conversation_history = []

def listen():
    """Listens for user input and returns the recognized text and detected language."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    command = None
    detected_language = None

    try:
        # Try English first
        command = r.recognize_google(audio, language='en-US').lower()
        detected_language = 'en'
        print(f"You said (English): {command}")
    except sr.UnknownValueError:
        try:
            # If English fails, try Indonesian
            command = r.recognize_google(audio, language='id-ID').lower()
            detected_language = 'id'
            print(f"You said (Indonesian): {command}")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that in either English or Indonesian.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return command, detected_language

def speak(text, lang='en'):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # Speed of speech
    if lang == 'id':
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ID-ID_ANDIKA_11.0')
    else:
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0')
    engine.say(text)
    engine.runAndWait()

def main():
    """Main function to run the assistant."""
    global conversation_history
    speak("Hello! I'm your assistant. How can I help you today?")
    conversation_history.append({'role': 'assistant', 'content': "Hello! I'm your assistant. How can I help you today?"})

    while True:
        command, detected_language = listen()

        if command:
            speak_lang = detected_language if detected_language else 'en' # Default to English if language not detected

            # Command handling
            if "create file" in command:
                speak("Sure, what would you like to name the file?", lang=speak_lang)
                file_name, _ = listen()
                if file_name:
                    response = actions.create_file(file_name)
                    speak(response, lang=speak_lang)

            elif "delete file" in command:
                speak("No problem, which file should I delete?", lang=speak_lang)
                file_name, _ = listen()
                if file_name:
                    response = actions.delete_file(file_name)
                    speak(response, lang=speak_lang)

            elif "create folder" in command:
                speak("Okay, what should I name the new folder?", lang=speak_lang)
                folder_name, _ = listen()
                if folder_name:
                    response = actions.create_folder(folder_name)
                    speak(response, lang=speak_lang)

            elif "delete folder" in command:
                speak("Alright, which folder do you want to remove?", lang=speak_lang)
                folder_name, _ = listen()
                if folder_name:
                    response = actions.delete_folder(folder_name)
                    speak(response, lang=speak_lang)

            elif "open" in command:
                app_name = command.replace("open", "").strip()
                response = actions.open_application(app_name)
                speak(response, lang=speak_lang)

            elif "read file" in command:
                speak("Which file would you like me to read?", lang=speak_lang)
                file_name, _ = listen()
                if file_name:
                    content = actions.read_file_content(file_name)
                    speak("I've read the file. Would you like me to read it out loud or summarize it?", lang=speak_lang)
                    choice, _ = listen()
                    if choice and "read" in choice:
                        speak("Here is the content of the file:", lang=speak_lang)
                        print(content)
                        speak(content, lang=speak_lang)
                    elif choice and "summarize" in choice:
                        summary = actions.summarize_text(content)
                        speak("Here is a summary of the file:", lang=speak_lang)
                        speak(summary, lang=speak_lang)
                        print(summary)

            elif "search for" in command:
                query = command.replace("search for", "").strip()
                speak(f"Searching for {query}...", lang=speak_lang)
                search_results = actions.web_search(query)
                print(search_results)
                speak(search_results, lang=speak_lang)

            elif "port scan" in command:
                speak("What is the target IP address?", lang=speak_lang)
                target, _ = listen()
                speak("What ports should I scan?", lang=speak_lang)
                ports, _ = listen()
                if target and ports:
                    scan_result = actions.port_scan(target, ports)
                    print(scan_result)
                    speak("Port scan complete. Results are in the console.", lang=speak_lang)

            elif "hash file" in command:
                speak("Which file should I hash?", lang=speak_lang)
                file_path, _ = listen()
                if file_path:
                    file_hash = actions.hash_file(file_path)
                    print(f"SHA-256 Hash: {file_hash}")
                    speak(f"The SHA-256 hash of the file is {file_hash}", lang=speak_lang)

            elif "run command" in command:
                speak("What command should I run?", lang=speak_lang)
                shell_command, _ = listen()
                if shell_command:
                    command_output = actions.run_command(shell_command)
                    print(command_output)
                    speak("Command executed. Output is in the console.", lang=speak_lang)

            elif "exit" in command or "quit" in command:
                speak("Goodbye! Have a great day!", lang=speak_lang)
                break

            else:
                # Fallback to conversational AI
                response = ollama_integration.get_ollama_response(command, conversation_history=conversation_history)
                speak(response, lang=speak_lang)
                conversation_history.append({'role': 'user', 'content': command})
                conversation_history.append({'role': 'assistant', 'content': response})

if __name__ == "__main__":
    main()