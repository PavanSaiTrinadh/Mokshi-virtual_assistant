import os
import webbrowser
import subprocess
import utilities
import ctypes
from time import sleep
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Social media handling function (now more generalized)
def social_media(social):
    try:
        # Remove spaces and capitalize the name correctly
        formatted_social = social.replace(" ", "").capitalize()
        app_path = f"C:\\Program Files\\{formatted_social}\\{formatted_social}.exe"
        if os.path.exists(app_path):
            os.startfile(app_path)
        else:
            if formatted_social == "Whatsapp":
                utilities.speak(f"{social} app not found. Opening in browser.")
                webbrowser.open('https://web.whatsapp.com/')
            else:
                utilities.speak(f"{social} app not found. Opening in browser.")
                webbrowser.open(f"https://{social}.com")


    except Exception as e:
        utilities.speak(f"An error occurred while opening {social}: {e}")

def open_camera():
    try:
        os.system("start microsoft.windows.camera")
    except Exception:
        print("Camera application is not available. Please check your system.")


# Open Command Prompt
def open_command_prompt():
    os.system("start cmd")

# Open File Explorer
def open_file_explorer():
    os.system("explorer")

def open_notepad():
    try:
        os.system("notepad")
    except Exception:
        print("Notepad could not be opened.")

def handle_shutdown_or_restart(query):
    if "shutdown" in query or "restart" in query:
        action = "shutdown" if "shutdown" in query else "restart"
        utilities.speak(f"Do you want me to {action} the computer?")
        confirmation = utilities.take_command().lower()
        if "yes" in confirmation:
            utilities.speak(f"{action.capitalize()}ing the computer.")
            os.system(f"shutdown /{action[0]} /t 5")  # Shutdown or restart in 5 seconds
        else:
            utilities.speak(f"{action.capitalize()} operation canceled.")

# Play Music
def play_music(music_path):
    subprocess.Popen(['start', music_path], shell=True)

# Write and Save a Note
def create_note(note_content, filename="note.txt"):
    # Get the current directory and ensure the file has a .txt extension
    if not filename.endswith(".txt"):
        filename += ".txt"
    file_path = os.path.join(os.getcwd(), filename)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(note_content)
        print(f"Note saved successfully as {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the note: {e}")

# Volume adjustment
VK_VOLUME_UP = 0xAF   # Volume Up key
VK_VOLUME_DOWN = 0xAE # Volume Down key

def adjust_volume(level):
    user32 = ctypes.windll.user32
    if level == "increase":
        for i in range(5):
            user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            sleep(0.1)
            user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
    elif level == "decrease":
        for i in range(5):
            user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            sleep(0.1)
            user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
    else:
        print("Invalid volume level. Use 'increase' or 'decrease'.")

# Open Calculator
def open_calculator():
    os.system("calc")

# Lock the Computer
def lock_computer():
    os.system("rundll32.exe user32.dll,LockWorkStation")

# Open Task Manager
def open_task_manager():
    os.system("taskmgr")

# Open a Website (e.g., YouTube)
def open_youtube():
    webbrowser.open("https://www.youtube.com")
    utilities.speak("Opening YouTube in browser")


import pyautogui
import os
import utilities  # Assuming utilities is a valid module


def open_application(query):
    try:
        utilities.speak("Please specify what you want to open.")
        query = utilities.take_command()
        # Press the 'Super' key (Windows key) to open the start menu
        pyautogui.press("super")
        # Type the application name or search term
        pyautogui.typewrite(query)
        # Wait for the search results to load
        pyautogui.sleep(2)
        # Press 'Enter' to open the application or search result
        pyautogui.press("enter")
        # Provide feedback to the user
        utilities.speak(f"Opening {query}...")
    except Exception as e:
        utilities.speak(f"An error occurred while trying to open {query}: {e}")
        print(f"Error: {e}")
