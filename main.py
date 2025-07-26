
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
    speak("Hello! I'm your assistant. How can I help you?")

    while True:
        command = listen()

        if command:
            if "create file" in command:
                speak("What should be the name of the file?")
                file_name = listen()
                if file_name:
                    response = actions.create_file(file_name)
                    speak(response)

            elif "delete file" in command:
                speak("What file do you want to delete?")
                file_name = listen()
                if file_name:
                    response = actions.delete_file(file_name)
                    speak(response)

            elif "create folder" in command:
                speak("What should be the name of the folder?")
                folder_name = listen()
                if folder_name:
                    response = actions.create_folder(folder_name)
                    speak(response)

            elif "delete folder" in command:
                speak("What folder do you want to delete?")
                folder_name = listen()
                if folder_name:
                    response = actions.delete_folder(folder_name)
                    speak(response)

            elif "open" in command:
                app_name = command.replace("open", "").strip()
                response = actions.open_application(app_name)
                speak(response)

            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break

            else:
                speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
