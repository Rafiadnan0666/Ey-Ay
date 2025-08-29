import pyttsx3
import queue
import threading
import json
import time

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.list_voices()  # Add this line to list voices on startup
        self.queue = queue.Queue()
        self.active = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run_engine, daemon=True)
        self.load_config()
        self.thread.start()

    def list_voices(self):
        """Lists all available voices and their properties."""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(f"ID: {voice.id}")
            print(f"  Name: {voice.name}")
            print(f"  Gender: {voice.gender}")
            print(f"  Languages: {voice.languages}")
            print(f"  Age: {voice.age}")

    def load_config(self):
        with open('config.json') as f:
            config = json.load(f)
            self.voice_config = config['config']['settings']['voice']

    def _configure_voice(self, lang='en'):
        """Configure voice settings based on language"""
        voice_id = self.voice_config['english_voice'] if lang == 'en' else self.voice_config['indonesian_voice']
        self.engine.setProperty('voice', voice_id)
        self.engine.setProperty('rate', self.voice_config['rate'])
        self.engine.setProperty('volume', self.voice_config['volume'])

    def _run_engine(self):
        """Main engine loop that processes speech queue"""
        self.active = True
        while self.active:
            try:
                item = self.queue.get(timeout=0.1)
                if item == 'SHUTDOWN':
                    break
                
                text, lang = item
                with self.lock:
                    self._configure_voice(lang)
                    self.engine.say(text)
                    self.engine.runAndWait()
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Voice engine error: {e}")

    def speak(self, text, lang='en'):
        """Add speech to the queue with Jarvis-like patterns"""
        if not text.strip():
            return
            
        # Add Jarvis personality traits
        if text.endswith('?'):
            text = f"{text[:-1]}, sir?"
        elif text.endswith('.'):
            text = f"{text[:-1]}, sir."
        elif not any(text.endswith(p) for p in ['!', '?', '.']):
            text = f"{text}, sir"
            
        self.queue.put((text, lang))

    def stop(self):
        """Clean shutdown of voice engine"""
        self.active = False
        self.queue.put('SHUTDOWN')
        self.thread.join()
        self.engine.stop()