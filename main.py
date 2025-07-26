
import speech_recognition as sr
import pyttsx3
import actions

def listen():
    """Listens for user input and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    """Main function to run the assistant."""
    speak("Hello! I'm your assistant. How can I help you today?")

    while True:
        command = listen()

        if command:
            if "create file" in command:
                speak("Sure, what would you like to name the file?")
                file_name = listen()
                if file_name:
                    response = actions.create_file(file_name)
                    speak(response)

            elif "delete file" in command:
                speak("No problem, which file should I delete?")
                file_name = listen()
                if file_name:
                    response = actions.delete_file(file_name)
                    speak(response)

            elif "create folder" in command:
                speak("Okay, what should I name the new folder?")
                folder_name = listen()
                if folder_name:
                    response = actions.create_folder(folder_name)
                    speak(response)

            elif "delete folder" in command:
                speak("Alright, which folder do you want to remove?")
                folder_name = listen()
                if folder_name:
                    response = actions.delete_folder(folder_name)
                    speak(response)

            elif "open" in command:
                app_name = command.replace("open", "").strip()
                response = actions.open_application(app_name)
                speak(response)

            elif "read file" in command:
                speak("Which file would you like me to read?")
                file_name = listen()
                if file_name:
                    content = actions.read_file_content(file_name)
                    speak("I've read the file. Would you like me to read it out loud or summarize it?")
                    choice = listen()
                    if choice and "read" in choice:
                        speak("Here is the content of the file:")
                        print(content)
                        speak(content)
                    elif choice and "summarize" in choice:
                        summary = actions.summarize_text(content)
                        speak("Here is a summary of the file:")
                        speak(summary)
                        print(summary)

            elif "exit" in command or "quit" in command:
                speak("Goodbye! Have a great day!")
                break

            else:
                speak("I'm not sure how to help with that. Can you try another command?")

if __name__ == "__main__":
    main()
