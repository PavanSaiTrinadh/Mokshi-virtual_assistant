import os
from email.message import EmailMessage
import smtplib
import requests
import wikipedia
import pywhatkit as pwk
import imdb
import wolframalpha as wa
import utilities
from dotenv import load_dotenv
import pyautogui
import datetime

# Load .env file
load_dotenv()

def music(song):
    pwk.playonyt(song)


# Google search
def search_on_google(query):
    try:
        pwk.search(query)
    except Exception as e:
        return f"Error performing Google search: {e}"


def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"


def youtube(video):
    pwk.playonyt(video)


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(receiver, sub, msg):
    try:
        email = EmailMessage()
        email['To'] = receiver
        email['Subject'] = sub
        email['From'] = EMAIL
        email.set_content(msg)
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(EMAIL, PASSWORD)
            s.send_message(email)
        return True
    except Exception as e:
        print(e)
        return False


def get_news():
    API_KEY = os.getenv("SERPAPI_KEY")  # Store securely
    params = {
        "q": "India",  # Query term
        "tbm": "nws",  # News tab
        "location": "India",  # Location filter
        "hl": "en",  # Language (English)
        "gl": "IN",  # Country code for India
        "api_key": API_KEY,
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        news_headlines = [article["title"] for article in data.get("news_results", [])]
        return news_headlines[:6] if news_headlines else ["No news found."]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return ["Unable to fetch news. Please try again later."]


WEATHER_FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_FORECAST_API_KEY = os.getenv("WEATHER_FORECAST_API_KEY") # Store securely


def weather_forecast(city):
    try:
        res = requests.get(
            WEATHER_FORECAST_API_URL,
            params={
                "q": city,
                "appid": WEATHER_FORECAST_API_KEY,
                "units": "metric"
            }
        )
        res.raise_for_status()
        data = res.json()
        if data.get("cod") == 200:
            weather = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            return weather, f"{temp}°C", f"{feels_like}°C"
        else:
            return "Unable to get weather information", "", ""
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}", "", ""


def movie():
    mvies_db = imdb.IMDb()
    utilities.speak("Please tell me the movie name: ")
    text = utilities.take_command()
    if text:
        movies = mvies_db.search_movie(text)
        utilities.speak("Searching for " + text)
        utilities.speak("I found these:")
        for movie in movies:
            title = movie["title"]
            year = movie["year"]
            utilities.speak(f"{title}: {year}")
            info = movie.getID()
            movie_info = mvies_db.get_movie(info)
            rating = movie_info["rating"]
            cast = movie_info["cast"]
            actor = cast[0:5]
            plot = movie_info.get('plot outline', 'Not available')
            utilities.speak(f"{title} was released in {year}, has IMDb ratings of {rating}. It stars {', '.join(actor)}. Plot: {plot}")
            print(f"{title} was released in {year}, has IMDb ratings of {rating}. It stars {', '.join(actor)}. Plot: {plot}")


def calculate(query):
    app_id = os.getenv("wolfram_app_id")  # Store securely
    client = wa.Client(app_id)
    try:
        ind = query.lower().split().index("calculate")
        text = query.split()[ind + 1:]
        result = client.query(" ".join(text))
        ans = next(result.results).text
        utilities.speak("The answer is " + ans)
        print("The answer is " + ans)
    except StopIteration:
        utilities.speak("I couldn't find that. Please try again.")
    except Exception as e:
        utilities.speak(f"Error: {str(e)}")
        print(f"Error: {str(e)}")

def open_new_tab():
    pyautogui.hotkey('ctrl', 't')
    return "Opened a new tab."

def close_tab():
    pyautogui.hotkey('ctrl', 'w')
    return "Closed the current tab."

def open_browser_menu():
    pyautogui.hotkey('alt', 'f')
    return "Opened the browser menu."

def zoom_in():
    pyautogui.hotkey('ctrl', '+')
    return "Zoomed in."

def zoom_out():
    pyautogui.hotkey('ctrl', '-')
    return "Zoomed out."

def refresh_page():
    pyautogui.hotkey('ctrl', 'r')
    return "Page refreshed."

def switch_to_next_tab():
    pyautogui.hotkey('ctrl', 'tab')
    return "Switched to the next tab."

def switch_to_previous_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    return "Switched to the previous tab."

def open_history():
    pyautogui.hotkey('ctrl', 'h')
    return "Opened browser history."

def open_bookmarks():
    pyautogui.hotkey('ctrl', 'shift', 'o')
    return "Opened bookmarks."

def go_back():
    pyautogui.hotkey('alt', 'left')
    return "Went back to the previous page."

def go_forward():
    pyautogui.hotkey('alt', 'right')
    return "Went forward to the next page."

def open_dev_tools():
    pyautogui.hotkey('ctrl', 'shift', 'i')
    return "Opened developer tools."

def toggle_full_screen():
    pyautogui.hotkey('f11')
    return "Toggled full screen mode."

def open_private_window():
    pyautogui.hotkey('ctrl', 'shift', 'n')
    return "Opened a private window."


def whatsapp_to_person():
    utilities.speak("Enter number")
    number = input("Enter number: ")  # Get number as a string
    utilities.speak("What message you want to send?")
    msg = input("Enter message: ")
    # Format the number with country code (+91 for India)
    formatted_number = "+91" + number
    # Send the message instantly using pywhatkit
    pwk.sendwhatmsg_instantly(formatted_number, msg)
    # Confirm the message has been sent
    utilities.speak(f"Message sent to {formatted_number}")


def scedule_whatsapp():
    # Ask for the recipient's phone number
    utilities.speak("Enter number")
    num = input("Enter number: ")  # Get number as a string
    # Ask for the message to send
    utilities.speak("What message you want to send?")
    msg = input("Enter message: ")
    # Ask for the time to send the message
    utilities.speak("At what hour should I send the message?")
    hr = int(input("Enter hour (24-hour format): "))
    utilities.speak("At what minute should I send the message?")
    min = int(input("Enter minute: "))
    # Send the message at the specified time
    formatted_number = "+91" + num
    pwk.sendwhatmsg(formatted_number, msg, hr, min)
    # Confirm the message has been sent
    utilities.speak(f"Message scheduled to be sent to {num} at {hr}:{min}.")



