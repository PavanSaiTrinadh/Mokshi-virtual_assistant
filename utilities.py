#utilities.py
import pyttsx3
from datetime import datetime
import pyjokes
import requests
import geocoder
import speech_recognition as sr
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np


from sqlalchemy.sql.functions import current_time

# Load .env file
load_dotenv()  # Initialize dotenv


# Initialize the speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female voice
# Function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to take a voice command
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"Error: {e}")
    return None

# Take voice input from user
def take_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)  # Speak the prompt to the user
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I didn't catch that. Can you repeat?")
            return None

# Task: Check the Time
def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."
def tell_date():
    current_date = datetime.now().strftime("%d:%m")
    return f"today's date is {current_date}."

# Task: Tell a Joke
def tell_joke():
    joke = pyjokes.get_joke()
    return joke

# Function to find the device's IP address
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def get_device_location():
    g = geocoder.ip('me')  # 'me' gets the current device's IP location
    return g.city  # Return city name

# Function to check microphone health
def check_microphone_health():
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Testing microphone. Please say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            print("Microphone is working fine!")
            return "Microphone is working fine."
    except Exception as e:
        print(f"Microphone test failed: {e}")
        return "Microphone is not working properly."

# Function to check speaker health
def check_speaker_health():
    try:
        duration = 3  # Duration in seconds
        fs = 44100  # Sample rate
        # Generate a test tone
        frequency = 440  # Frequency in Hz (A4 tone)
        time = np.linspace(0, duration, int(fs * duration), endpoint=False)
        test_tone = 0.5 * np.sin(2 * np.pi * frequency * time)

        # Play the test tone
        print("Testing speakers. You should hear a tone...")
        sd.play(test_tone, samplerate=fs)
        sd.wait()
        print("Speaker test completed successfully.")
        return "Speaker is working fine."
    except Exception as e:
        print(f"Speaker test failed: {e}")
        return "Speaker is not working properly."


import os


def find_file_or_folder(name, search_path="/"):
    results = []
    for root, dirs, files in os.walk(search_path, onerror=lambda e: None):  # Safeguard against inaccessible directories
        # Check for matching directories
        for dir_name in dirs:
            if name == dir_name:
                results.append(os.path.join(root, dir_name))
        # Check for matching files
        for file_name in files:
            if name == file_name:
                results.append(os.path.join(root, file_name))
    return results



