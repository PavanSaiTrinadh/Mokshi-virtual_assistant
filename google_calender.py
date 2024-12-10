import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import utilities

# Scopes define the level of access. Adjust as needed.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Authenticate and get credentials for Google Calendar API
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


# Create a new event
def create_calendar_event():
    utilities.speak("What is the event name?")
    event_name = input("Enter event name: ")
    if not event_name:
        return

    utilities.speak("On which date should I schedule it?")
    event_date = input("Please enter in YYYY-MM-DD format:")
    if not event_date:
        return

    utilities.speak("At what time?")
    event_time = input("Please enter in HH:MM 24-hour format.")
    if not event_time:
        return

    event_description = input("Enter description")


    try:
        event_start_time = datetime.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
        event_end_time = event_start_time + datetime.timedelta(hours=1)  # Default duration of 1 hour
    except ValueError:
        utilities.speak("The date or time format was incorrect. Please try again.")
        return

    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        event = {
            'summary': event_name,
            'description': event_description,
            'start': {
                'dateTime': event_start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': event_end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        utilities.speak(f"Event '{event_name}' has been added to your calendar.")
        print(f"Event created: {created_event.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        utilities.speak("There was an error adding the event to your calendar.")


def get_upcoming_events():
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow()
        now_start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        now_iso = now.isoformat() + "Z"  # 'Z' indicates UTC time

        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now_iso,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            utilities.speak("No upcoming events found.")
            print("No upcoming events found.")
        else:
            utilities.speak("Here are your upcoming events:")
            for event in events:
                start_time = event["start"].get("dateTime", event["start"].get("date"))
                event_datetime = datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))

                # Format event details
                event_day = event_datetime.strftime("%Y-%m-%d")
                event_time = event_datetime.strftime("%I:%M %p")
                event_summary = event.get('summary', 'No Title')

                # Check if the event is today
                if event_day == now_start_of_day.strftime("%Y-%m-%d"):
                    utilities.speak(f"You have an event named {event_summary} today at {event_time}.")
                else:
                    formatted_date = event_datetime.strftime("%d %B")  # Example: "11th December"
                    utilities.speak(f"On {formatted_date}, you have an event named {event_summary} at {event_time}.")

                # Print event details for debugging
                print(f"Event: {event_summary}, Date: {event_day}, Time: {event_time}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        utilities.speak("There was an error fetching your events.")


# Check today's events and notify
def check_and_notify_events():
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + datetime.timedelta(days=1)

        events_result = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat() + 'Z',
            timeMax=(today_start + datetime.timedelta(days=7)).isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            utilities.speak("You have no events scheduled for today.")
        else:
            utilities.speak("Here are your upcoming events:")
            for event in events:
                # Parse event start time
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                event_datetime = datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))

                # Determine the event day
                event_day = event_datetime.strftime("%Y-%m-%d")
                event_time = event_datetime.strftime("%I:%M %p")
                event_summary = event.get('summary', 'No Title')

                # Check if the event is today
                if event_day == today_start.strftime("%Y-%m-%d"):
                    utilities.speak(f"You have an event named {event_summary} today at {event_time}.")
                else:
                    formatted_date = event_datetime.strftime("%d %B")  # Example: "11th December"
                    utilities.speak(f"On {formatted_date}, you have an event named {event_summary} at {event_time}.")

                # Print event details for debugging
                print(f"Event: {event_summary}, Date: {event_day}, Time: {event_time}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        utilities.speak("There was an error fetching your events.")

