import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds=None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")     

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
            creds=flow.run_local_server(port=0)
        
        with open("token.json","w") as token:
            token.write(creds.to_json())
    try:
        service=build("calendar","v3",credentials=creds)
        while True:
            user_input = input("Enter a command (type 'EXIT' to quit): ")
            if user_input == "EXIT":
                break
            else:
                print(f"Unknown command '{user_input}'")
                event = {
                    "summary": input("Enter the title of the event: "),
                    "location": input("Enter the location of the event: "),
                    "description": input("Enter the description to the event: "),
                    "start": {
                        "dateTime": "2023-10-23T09:00:00+05:30",
                        "timeZone": "Asia/Kolkata"
                    },
                    "end": {
                        "dateTime": "2023-10-25T17:00:00+05:30",
                        "timeZone": "Asia/Kolkata"
                    },
                    "recurrence": [
                        "RRULE:FREQ=DAILY;COUNT=1"
                    ],
                    "attendees": [
                        {"email": "sant.raj18@gmail.com"},
                    ]        
                }

                event = service.events().insert(calendarId="primary", body=event).execute()
            
                print("Event created ", event.get('htmlLink'))

    except HttpError as error:
        print("An error occurred:", error)

if __name__=="__main__":
    main()

