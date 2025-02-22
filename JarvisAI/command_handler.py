# command_handler.py
import os
import subprocess
import psutil  # For closing apps
import webbrowser
from config import APP_PATHS, BROWSERS, PROCESS_NAMES

class CommandHandler:
    @staticmethod
    def open_app(app_name: str) -> str:
        """Open applications like Chrome, Notepad, etc."""
        app_name = app_name.lower()
        for key, path in APP_PATHS.items():
            if key in app_name:
                try:
                    subprocess.Popen([path])  # Faster than os.startfile()
                    return f"Opening {key.capitalize()}..."
                except Exception as e:
                    return f"Failed to open {key}. Error: {e}"
        return "Application not supported."

    @staticmethod
    def close_app(app_name: str) -> str:
        """Close applications by process name."""
        app_name = app_name.lower()
        for key, process in PROCESS_NAMES.items():
            if key in app_name:
                try:
                    for proc in psutil.process_iter():
                        if proc.name().lower() == process.lower():
                            proc.kill()
                    return f"Closed {key.capitalize()}."
                except Exception as e:
                    return f"Failed to close {key}. Error: {e}"
        return "Application not found."

    @staticmethod
    def open_url(url: str, browser: str = "chrome") -> str:
        """Open URLs in a specified browser."""
        try:
            url = url.strip().replace(" ", "")
            if "youtube" in url:
                url = "https://www.youtube.com"
            elif "google" in url:
                url = "https://www.google.com"

            # Open in specified browser
            if browser in BROWSERS:
                subprocess.Popen([BROWSERS[browser], "--new-tab", url])
                return f"Opening {url} in {browser.capitalize()}..."
            else:
                webbrowser.open(url)
                return f"Opening {url}..."
        except Exception as e:
            return f"Failed to open {url}. Error: {e}"