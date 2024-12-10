import google_calender as gc
from datetime import datetime
import keyboard
import pyautogui
from dotenv import load_dotenv
# Load .env file
load_dotenv()

import automation
import online
import utilities
import genai_integration
import os

# Define user and hostname
username = os.getenv("USERNAME")
HOSTNAME = "Mokshi"
listening = False


# Retrieve username from .env
'''def get_username():
    username = os.getenv("USERNAME")
    if not username:
        utilities.speak("Hello! It seems this is our first interaction. May I know your name?")
        username = utilities.take_command()
        if username:
            utilities.speak(f"Nice to meet you, {username}!")
            # Save username to the .env file if you want it persisted
            with open(".env", "a") as env_file:
                env_file.write(f"\nUSERNAME={username}")
        else:
            utilities.speak("I didn't catch your name. I'll call you User for now.")
            username = "User"
    return username'''

# Function to greet the user
def greet(username):
    hour = datetime.now().hour
    greeting = (
        "Good Morning"
        if 6 <= hour < 12
        else "Good Afternoon"
        if 12 <= hour < 16
        else "Good Evening"
    )
    utilities.speak(f"{greeting}, {username}. I am {HOSTNAME}. How can I assist you today?")

# Start and pause listening
def start_listening():
    global listening
    listening = True
    print("Listening started")

def pause_listening():
    global listening
    listening = False
    print("Listening stopped")

# Hotkeys to control listening
keyboard.add_hotkey('ctrl+alt+z', start_listening)
keyboard.add_hotkey('ctrl+alt+x', pause_listening)

# Main listening loop
if __name__ == '__main__':
    #username = get_username()
    greet(username)
    while True:
        if listening:
            query = utilities.take_command()
            if query:
                if "how are you" in query:
                    utilities.speak(f"I'm doing great, {username}! How about you?")
                elif "exit" in query or "quit" in query:
                    utilities.speak(f"Goodbye, {username}!")
                    break
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("mokshi","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                elif "lock computer" in query:
                    automation.lock_computer()
                elif "shutdown" in query or "restart" in query:
                    automation.handle_shutdown_or_restart(query)
                elif "volume" in query:
                    if "increase" in query:
                        automation.adjust_volume("increase")
                        utilities.speak("Volume increased by 10 percent")
                    elif "decrease" in query:
                        automation.adjust_volume("decrease")
                        utilities.speak("Volume decreased by 10 percent")

                elif "search on google" in query:
                    utilities.speak("What should I search for?")
                    search_query = utilities.take_command()
                    if search_query:
                        online.search_on_google(search_query)
                        utilities.speak(f"Here are the search results for {search_query}.")
                elif "what's the time" in query:
                    time_message = utilities.tell_time()
                    utilities.speak(time_message)
                elif "what is today's date" in query:
                    date_message = utilities.tell_date()
                    utilities.speak(date_message)

                elif "device location" in query:
                    a = utilities.get_device_location()
                    utilities.speak(a)
                elif "play music" in query:
                    utilities.speak("What music should I play?")
                    music_path = utilities.take_command()  # Specify the music path
                    if music_path:
                        automation.play_music(music_path)
                        utilities.speak("Playing music now.")
                elif "tell me a joke" in query:
                    joke = utilities.tell_joke()
                    utilities.speak(joke)
                elif "weather update" in query:
                    city = utilities.get_device_location()
                    if city:
                        weather, temp, feels_like = online.weather_forecast(city)
                        utilities.speak(f"Weather in {city}: {weather}, Temperature: {temp}, Feels Like: {feels_like}")
                    else:
                        utilities.speak("Unable to detect location.")
                elif "movie" in query:
                    online.movie()
                elif "calculate" in query: #not working
                    online.calculate(query)
                elif "create a note" in query:
                    utilities.speak("What would you like to note down?")
                    content = utilities.take_command()
                    utilities.speak("Enter a filename (or press Enter for default): ").strip()
                    filename = input("Enter a filename (or press Enter for default): ")
                    automation.create_note(content, filename if filename else "note.txt")
                elif "give me news" in query:
                    news = online.get_news()
                    utilities.speak("Today's top headlines are:")
                    for headline in news:
                        utilities.speak(headline)
                    print("\n".join(news))
                elif "send email" in query:
                    utilities.speak("Enter the recipient's email address:")
                    receiver = input("Email Address: ")
                    utilities.speak("What should be the subject?")
                    subject = input("Enter subject: ")
                    utilities.speak("What is the message?")
                    message = input("Enter message: ")
                    if online.send_email(receiver, subject, message):
                        utilities.speak("Email sent successfully.")
                    else:
                        utilities.speak("Something went wrong while sending the email.")
                elif "ip address" in query:
                    utilities.speak(utilities.find_my_ip())
                elif "wikipedia" in query:
                    utilities.speak("What do you want to search on Wikipedia?")
                    search = utilities.take_command().lower()
                    results = online.search_on_wikipedia(search)
                    utilities.speak(f"According to Wikipedia, {results}")
                    utilities.speak("I am printing it on the terminal")
                    print(results)
                elif "check microphone" in query:
                    microphone_status = utilities.check_microphone_health()
                    utilities.speak(microphone_status)

                elif "check speaker" in query:
                    speaker_status = utilities.check_speaker_health()
                    utilities.speak(speaker_status)
                elif "new tab" in query or "new tab kholo" in query:
                    response = online.open_new_tab()
                    utilities.speak(response)

                elif "close tab" in query or "tab band karo" in query:
                    response = online.close_tab()
                    utilities.speak(response)

                elif "browser menu" in query or "browser menu kholo" in query:
                    response = online.open_browser_menu()
                    utilities.speak(response)

                elif "zoom in" in query or "zoom in karo" in query:
                    response = online.zoom_in()
                    utilities.speak(response)

                elif "zoom out" in query or "zoom out karo" in query:
                    response = online.zoom_out()
                    utilities.speak(response)

                elif "refresh page" in query or "page refresh karo" in query:
                    response = online.refresh_page()
                    utilities.speak(response)

                elif "switch to next tab" in query or "next tab par jao" in query:
                    response = online.switch_to_next_tab()
                    utilities.speak(response)

                elif "switch to previous tab" in query or "previous tab par jao" in query:
                    response = online.switch_to_previous_tab()
                    utilities.speak(response)

                elif "open history" in query or "history kholo" in query:
                    response = online.open_history()
                    utilities.speak(response)

                elif "open bookmarks" in query or "bookmarks kholo" in query:
                    response = online.open_bookmarks()
                    utilities.speak(response)

                elif "go back" in query or "peeche jao" in query:
                    response = online.go_back()
                    utilities.speak(response)

                elif "go forward" in query or "aage jao" in query:
                    response = online.go_forward()
                    utilities.speak(response)

                elif "open dev tools" in query or "dev tools" in query:
                    response = online.open_dev_tools()
                    utilities.speak(response)

                elif "toggle full screen" in query or "full screen" in query:
                    response = online.toggle_full_screen()
                    utilities.speak(response)

                elif "open private window" in query or "private window" in query:
                    response = online.open_private_window()
                    utilities.speak(response)

                elif "create event" in query:
                    gc.create_calendar_event()
                elif "get events" in query or "upcoming events" in query:
                    gc.get_upcoming_events()
                elif "today's events" in query or "notify" in query:
                    gc.check_and_notify_events()

                elif "send message" in query:
                    online.whatsapp_to_person()
                elif "schedule message" in query:
                    online.scedule_whatsapp()
                elif "search file" in query or "search a folder" in query:
                    utilities.speak("Enter the file or folder name to search for?")
                    search_name = input("Enter the file or folder name to search for: ")
                    matches = utilities.find_file_or_folder(search_name)
                    if matches:
                        print(f"Found {len(matches)} result(s):")
                        for match in matches:
                            print(match)
                    else:
                        print("No matches found.")
                else:
                    gemini_response = genai_integration.response_of_gemini(query)
                    gemini_response = gemini_response.replace("*", "")
                    if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                        utilities.speak(gemini_response)
                        print(gemini_response)
