# jarvis.py
from speech import SpeechEngine
from command_handler import CommandHandler

class Jarvis:
    def __init__(self):
        self.speech_engine = SpeechEngine()
        self.handler = CommandHandler()

    def run(self):
        self.speech_engine.speak("Hello, I am your assistant. How can I help you?")
        while True:
            command = self.speech_engine.take_command()
            if not command:
                continue

            # Open/Close Applications
            if "open" in command:
                if " in " in command:
                    # Handle "open [url] in [browser]"
                    parts = command.split(" in ")
                    target = parts[0].replace("open", "").strip()
                    browser = parts[1].strip()
                    response = self.handler.open_url(target, browser)
                else:
                    app_name = command.replace("open", "").strip()
                    response = self.handler.open_app(app_name)
                self.speech_engine.speak(response)

            elif "close" in command:
                app_name = command.replace("close", "").strip()
                response = self.handler.close_app(app_name)
                self.speech_engine.speak(response)

            elif "exit" in command or "quit" in command:
                self.speech_engine.speak("Goodbye!")
                break

if __name__ == "__main__":
    assistant = Jarvis()
    assistant.run()