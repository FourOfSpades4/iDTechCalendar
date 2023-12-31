# iDTechCalendar

Simple program to add all scheduled from iDTech to Google Calendar to make it easy to access and view.


## Setup
- Clone the repository: `git clone https://github.com/FourOfSpades4/iDTechCalendar.git`
- Make sure Python is installed
- Install [Requests](https://pypi.org/project/requests/) through `pip install requests`
- Install [Selenium](https://selenium-python.readthedocs.io/installation.html) through `pip install selenium`
  - This uses Selenium Firefox, not Chrome. You can edit it for Chrome if you'd like
  - Edit: I was told to mention that no, it does not work if you don't have Firefox. It's using Selenium Firefox, which is a webdriver for **Firefox**. If you'd like to change it to use a different browser, it's not super difficult. Just edit the imports and swap the createDriver() method. You'll also need to download the [Chrome Driver](https://chromedriver.chromium.org/downloads).
- Setup [Google Calendar API](https://developers.google.com/calendar/api/quickstart/python) for Python
  - Paste `credentials.json` file in the directory containing `main.py`
- Create a new Google Calendar that will only be used for iDTech Events.
- Copy the CalendarID (Settings -> Calendar Name -> Integrate Calendar -> Copy CalendarID)

- In [main.py](main.py):
  - Paste CalendarID where it says `calendarID = ""`
  - Change Time Zone to your iDTech Calendar Time Zone
 
## Running the Program
- Run `main.py`
- A Firefox window should open. Login to iDTech.
- Once logged in, hit "Enter" in the console
- It may prompt you to login to google. If it does, login with the same account used to setup the Google Calendar API.
- That's it! The calendar should be populated with the next ~120 days of classes you are scheduled for.
  Running the program again will clear all previously added classes to prevent duplicate events if your schedule changes.
