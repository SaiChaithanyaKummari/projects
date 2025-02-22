# config.py

# App paths (customize these for your system)
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "spotify": r"C:\Users\YOUR_USERNAME\AppData\Roaming\Spotify\Spotify.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

# Browser names mapped to their executable paths
BROWSERS = {
    "chrome": APP_PATHS["chrome"],
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
}

# Keywords for closing apps
PROCESS_NAMES = {
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "spotify": "Spotify.exe",
}