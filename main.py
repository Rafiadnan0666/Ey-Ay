import speech_recognition as sr
import actions
import ollama_integration
import json
import asyncio
from voice_engine import VoiceEngine
from autonomous_agent import AutonomousAgent

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

async def main():
    """Main function to run the assistant."""
    global conversation_history
    voice = VoiceEngine()
    voice.speak("Hello! I'm Jarvis. How can I help you today?")
    conversation_history.append({'role': 'assistant', 'content': "Hello! I'm Jarvis. How can I help you today?"})

    while True:
        command, detected_language = await asyncio.to_thread(listen)

        if command:
            print(f"Command recognized: {command}")
            speak_lang = detected_language if detected_language else 'en' # Default to English if language not detected

            if "exit" in command or "quit" in command:
                voice.speak("Goodbye! Have a great day!", lang=speak_lang)
                print("Speaking: Goodbye! Have a great day!")
                break

            if "jarvis enter autonomous mode" in command:
                voice.speak("Autonomous mode activated. Please state your goal.", lang=speak_lang)
                print("Speaking: Autonomous mode activated. Please state your goal.")
                goal, _ = await asyncio.to_thread(listen)
                if goal:
                    agent = AutonomousAgent(conversation_history)
                    response = await agent.run(goal)
                    voice.speak(response, lang=speak_lang)
                    print(f"Speaking: {response}")
                continue

            # Fallback to conversational AI
            print(f"Sending to Ollama: {command}")
            llm_response = await asyncio.to_thread(ollama_integration.get_ollama_response, command, conversation_history=conversation_history)
            print(f"Received from Ollama: {llm_response}")
            
            try:
                # Attempt to parse the LLM's response as JSON
                parsed_response = json.loads(llm_response)
                print(f"Ollama response parsed as JSON: {parsed_response}")
                action = parsed_response.get("action")
                argument = parsed_response.get("argument")

                if hasattr(actions, action):
                    action_func = getattr(actions, action)
                    if asyncio.iscoroutinefunction(action_func):
                        response = await action_func(argument)
                    else:
                        response = await asyncio.to_thread(action_func, argument)
                    print(f"Action response: {response}")
                    voice.speak(response, lang=speak_lang)
                    print(f"Speaking: {response}")
                else:
                    # If JSON but unknown action, treat as conversational
                    voice.speak(llm_response, lang=speak_lang)
                    print(f"Speaking (unknown action): {llm_response}")
                    conversation_history.append({'role': 'user', 'content': command})
                    conversation_history.append({'role': 'assistant', 'content': llm_response})
            except json.JSONDecodeError:
                print("Ollama response is not valid JSON. Treating as conversational.")
                # If not JSON, treat as conversational
                voice.speak(llm_response, lang=speak_lang)
                print(f"Speaking (conversational): {llm_response}")
                conversation_history.append({'role': 'user', 'content': command})
                conversation_history.append({'role': 'assistant', 'content': llm_response})
        else:
            print("No command recognized.")
    
    voice.stop()

if __name__ == "__main__":
    asyncio.run(main())