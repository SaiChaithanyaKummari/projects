import speech_recognition as sr
import time
from pydub import AudioSegment
import os

def record_and_transcribe():
    """
    Simple function to record from microphone and transcribe
    """
    # Create a recognizer object
    recognizer = sr.Recognizer()
    
    # Use the microphone as audio source
    with sr.Microphone() as source:
        print("Please wait... calibrating microphone for ambient noise")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Microphone ready!")
        
        print("Speak now. The recording will stop automatically when you pause.")
        audio_data = recognizer.listen(source)
        
        print("Processing your speech...")
        
        try:
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said"
        except sr.RequestError:
            return "Sorry, there was an error with the speech service"

def transcribe_from_file(recognizer):
    """
    Transcribes audio from a user-provided file path.
    Handles WAV, FLAC, AIFF, and MP3 files.
    """
    file_path = input("Enter the path to the audio file (WAV/FLAC/AIFF/MP3): ")
    
    file_ext = os.path.splitext(file_path)[1].lower()

    if not os.path.exists(file_path):
        return f"File not found at: {file_path}"

    try:
        if file_ext == ".mp3":
            try:
                # Convert MP3 to WAV
                audio = AudioSegment.from_mp3(file_path)
                wav_path = "temp_audio.wav"
                audio.export(wav_path, format="wav")
                file_path = wav_path
            except FileNotFoundError:
                return "Error: FFmpeg not found. Please install FFmpeg and add it to your system's PATH to process MP3 files."
        
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        if file_ext == ".mp3":
            os.remove(wav_path) # Clean up the temporary WAV file

        return text
    except FileNotFoundError:
        return f"File not found at: {file_path}"
    except sr.UnknownValueError:
        return "Could not understand the audio in the file."
    except sr.RequestError:
        return "Could not get results from the speech service."
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    print("=== Simple Speech-to-Text Tool ===")
    recognizer = sr.Recognizer()

    while True:
        print("1. Record and transcribe from microphone")
        print("2. Transcribe from an audio file")
        print("3. Exit")
        choice = input("Choose an option (1, 2, or 3): ")

        if choice == "1":
            print("\nStarting recording...")
            transcription = record_and_transcribe()
            print("\nTranscription Result:")
            print(transcription)
        elif choice == "2":
            print("\nTranscribing from file...")
            transcription = transcribe_from_file(recognizer)
            print("\nTranscription Result:")
            print(transcription)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
        print("-" * 20)

if __name__ == "__main__":
    main()