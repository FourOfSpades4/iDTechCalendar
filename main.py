import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import sys

days = 120
SCOPES = ["https://www.googleapis.com/auth/calendar"]
calendarID = ""
timeZone = "America/New_York"

def createDriver(headless=True, javascript=True):
    options = Options()
    options.headless = headless
    options.set_preference('javascript.enabled', javascript)
    s = Service("geckodriver.exe")
    return webdriver.Firefox(options=options, service=s)

def getAuth(guid, userID):
    url = "https://pulseapi.idtech.com/token"
    data = {"grant_type":"token", "guid":guid, "userid":userID}
    response = requests.post(url, data=data)
    return json.loads(response.text)

def getSchedule():
    driver = createDriver(headless=False, javascript=False)
    try:
        driver.get("https://admin.idtech.com/PulseAdmin/Login.aspx")

        input()

        driver.get("https://admin.idtech.com/PulseAdmin/PagesAdmin/opl/oplteach_tabavailability.aspx?sr=2")
        for line in driver.page_source.split("\n"):
            if """data: "grant_type""" in line:
                line = line.strip()
                data = line.split("=")
                instructorID = data[3][:-2]
                auth = getAuth(data[2][:-7], instructorID)
                
                url = f"https://pulseapi.idtech.com/pulseWebApi/OnlinePrivateLesson_GetOPLInstructorAvailability?instructorUserID={instructorID}&daysBackward=0&daysForward={days}&dateString="
                headers = {"Authorization": "Bearer " + auth["access_token"]}
                response = requests.get(url, headers=headers)

                with open("schedule.json", "w") as f:
                    f.write(response.text)

    finally:
        driver.quit()

def parseSchedule():
    bookedSlots = []

    with open("schedule.json", "r") as f:
        schedule = json.loads(f.read())
        
        for slot in schedule["availabilities"]:
            if slot["text"]:
                bookedSlots.append((slot["text"], slot["startTime"], slot["endTime"]))

    return bookedSlots


def createEvents(events):
    creds = None
    if os.path.exists('tokens.json'):
        creds = Credentials.from_authorized_user_file('tokens.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        page_token = None
        while True:
            cal = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
            for event in cal['items']:
                service.events().delete(calendarId=calendarID, eventId=event["id"]).execute()
            page_token = cal.get('nextPageToken')
            if not page_token:
                break

        for event in events:
            toAdd = {
                'summary': event[0],
                'start': {
                    'dateTime': event[1],
                    'timeZone': timeZone,
                },
                'end': {
                    'dateTime': event[2],
                    'timeZone': timeZone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }

            event = service.events().insert(calendarId=calendarID, body=toAdd).execute()


    except HttpError as error:
        print('An error occurred: %s' % error)



if __name__ == "__main__":
    getSchedule()
    events = parseSchedule()
    createEvents(events)