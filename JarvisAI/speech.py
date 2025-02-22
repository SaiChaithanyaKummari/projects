# speech.py
import speech_recognition as sr
import pyttsx3

class SpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)  # Faster speech

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self) -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=4)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return "Speech service down."
            except sr.WaitTimeoutError:
                return ""