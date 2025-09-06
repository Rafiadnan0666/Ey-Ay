import speech_recognition as sr
import actions
import ollama_integration
import json
import asyncio
import os
import time
import threading
from datetime import datetime
from voice_engine import VoiceEngine
from autonomous_agent import AutonomousAgent
from typing import List, Dict, Any
import pyautogui
import keyboard
import subprocess

# Global variable to store conversation history
conversation_history = []
MEMORY_FILE = "ai_memory.json"

class AdvancedAssistant:
    def __init__(self):
        self.voice = VoiceEngine()
        self.agent = AutonomousAgent(conversation_history)
        self.current_tasks = []
        self.load_memory()
        
    def load_memory(self):
        """Load conversation history from memory file"""
        global conversation_history
        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conversation_history = data.get('conversation_history', [])
                    print(f"Loaded {len(conversation_history)} past conversations from memory")
        except Exception as e:
            print(f"Error loading memory: {e}")
            conversation_history = []
    
    def save_memory(self):
        """Save conversation history to memory file"""
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'conversation_history': conversation_history,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def listen(self):
        """Listens for user input and returns the recognized text and detected language."""
        print("Entering listen method...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening for audio...")
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=15)
                print("Audio captured, now recognizing...")
            except sr.WaitTimeoutError:
                print("Listening timed out. Please check your microphone and ensure you are speaking clearly.")
                return None, None
            except Exception as e:
                print(f"Error during listening: {e}")
                return None, None

        command = None
        detected_language = None

        try:
            # Try English first
            command = r.recognize_google(audio, language='en-US').lower()
            detected_language = 'en'
            print(f"You said (English): {command}")
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            try:
                # If English fails, try Indonesian
                command = r.recognize_google(audio, language='id-ID').lower()
                detected_language = 'id'
                print(f"You said (Indonesian): {command}")
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                print("Sorry, I didn't catch that in either English or Indonesian.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        return command, detected_language
    
    def execute_system_command(self, command: str):
        """Execute system commands"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else result.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def simulate_typing(self, text: str):
        """Simulate typing on the keyboard"""
        # Focus on the active window
        pyautogui.click(100, 100)  # Click to ensure focus
        
        # Type the text
        pyautogui.write(text, interval=0.01)
        
    def search_windows(self, query: str):
        """Simulate Windows search and open applications"""
        # Open Windows search
        keyboard.press_and_release('win+s')
        time.sleep(0.5)
        
        # Type the search query
        self.simulate_typing(query)
        time.sleep(0.5)
        
        # Press enter to execute
        keyboard.press_and_release('enter')
        
        return f"Searching for and opening {query}"

    async def handle_special_commands(self, command: str, lang: str):
        if "autonomous mode" in command.lower():
            return await self.activate_autonomous_mode(command, lang)
        
        if "search for" in command.lower() or "open " in command.lower():
            if "search for" in command.lower():
                query = command.lower().split("search for")[1].strip()
            else:
                query = command.lower().split("open ")[1].strip()
            
            result = self.search_windows(query)
            self.voice.speak(f"Searching for {query}", lang=lang)
            return result
        
        if "type " in command.lower():
            text_to_type = command.lower().split("type ")[1].strip()
            self.simulate_typing(text_to_type)
            self.voice.speak(f"Typing: {text_to_type}", lang=lang)
            return f"Typed: {text_to_type}"
        
        if "execute " in command.lower():
            cmd = command.lower().split("execute ")[1].strip()
            result = self.execute_system_command(cmd)
            self.voice.speak(f"Executed command: {cmd}", lang=lang)
            return f"Command executed. Result: {result}"

        if " and then " in command.lower():
            commands = command.lower().split(" and then ")
            results = []
            for cmd in commands:
                result = await self.process_command(cmd.strip(), lang)
                results.append(result)
                await asyncio.sleep(1)
            return "Completed all tasks: " + "; ".join(results)

        return None

    async def handle_ollama_response(self, llm_response: str, lang: str):
        try:
            parsed_response = json.loads(llm_response)
            action = parsed_response.get("action")
            argument = parsed_response.get("argument")
            
            if action and hasattr(actions, action):
                action_func = getattr(actions, action)
                if asyncio.iscoroutinefunction(action_func):
                    response = await action_func(argument)
                else:
                    response = await asyncio.to_thread(action_func, argument)
                
                conversation_history.append({
                    'role': 'assistant', 
                    'content': response,
                    'action': action,
                    'timestamp': datetime.now().isoformat()
                })
                
                self.voice.speak(response, lang=lang)
                return response
            else:
                self.voice.speak(llm_response, lang=lang)
                conversation_history.append({
                    'role': 'assistant', 
                    'content': llm_response,
                    'timestamp': datetime.now().isoformat()
                })
                return llm_response
                
        except json.JSONDecodeError:
            self.voice.speak(llm_response, lang=lang)
            conversation_history.append({
                'role': 'assistant', 
                'content': llm_response,
                'timestamp': datetime.now().isoformat()
            })
            return llm_response

    async def process_command(self, command: str, lang: str = 'en'):
        """Process user command with advanced capabilities"""
        global conversation_history
        
        try:
            conversation_history.append({'role': 'user', 'content': command, 'timestamp': datetime.now().isoformat()})
            
            response = await self.handle_special_commands(command, lang)
            if response:
                return response

            print(f"Sending to Ollama: {command}")
            llm_response = await asyncio.to_thread(
                ollama_integration.get_ollama_response, 
                command, 
                conversation_history=conversation_history
            )
            print(f"Received from Ollama: {llm_response}")
            
            return await self.handle_ollama_response(llm_response, lang)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.voice.speak("Sorry, I encountered an error.", lang=lang)
            return f"Error: {e}"
    
    async def activate_autonomous_mode(self, command: str, lang: str):
        """Activate autonomous mode for complex tasks"""
        self.voice.speak("Autonomous mode activated. Please state your goal.", lang=lang)
        print("Speaking: Autonomous mode activated. Please state your goal.")
        
        goal, _ = await asyncio.to_thread(self.listen)
        if goal:
            response = await self.agent.run(goal)
            
            conversation_history.append({
                'role': 'user', 
                'content': f"Autonomous mode goal: {goal}",
                'timestamp': datetime.now().isoformat()
            })
            conversation_history.append({
                'role': 'assistant', 
                'content': response,
                'autonomous': True,
                'timestamp': datetime.now().isoformat()
            })
            
            self.voice.speak(response, lang=lang)
            return response
        return "No goal specified for autonomous mode."
    
    async def run(self):
        """Main run loop for the assistant"""
        self.voice.speak("Hello! I'm your advanced AI assistant. How can I help you today?")
        conversation_history.append({
            'role': 'assistant', 
            'content': "Hello! I'm your advanced AI assistant. How can I help you today?",
            'timestamp': datetime.now().isoformat()
        })

        while True:
            command, detected_language = await asyncio.to_thread(self.listen)
            speak_lang = detected_language if detected_language else 'en'

            if command:
                if "exit" in command or "quit" in command or "goodbye" in command:
                    self.voice.speak("Goodbye! Have a great day!", lang=speak_lang)
                    break
                
                response = await self.process_command(command, speak_lang)
                print(f"Assistant: {response}")
                
                self.save_memory()
            else:
                print("No command recognized. Please try again.")
        
        self.voice.stop()

async def main():
    """Main function to run the assistant."""
    assistant = AdvancedAssistant()
    await assistant.run()

if __name__ == "__main__":
    asyncio.run(main())