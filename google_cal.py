import pprint

from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime


class GoogleCalendar:
    SCOPES=["https://www.googleapis.com/auth/calendar"]
    FILE_PATH='studied-jigsaw-404516-d3905d991705.json'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename=self.FILE_PATH, scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {'id': calendar_id}
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, body):
        return self.service.events().insert(calendarId=calendar_id, body=body).execute()

    def delete_event(self, calendar_id, event_id):
        return self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

    def get_event(self, calendar_id, event_id):
        return self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()


obj = GoogleCalendar()
#pprint.pprint(obj.get_calendar_list())

calendar_id = 'bukhantcev@gmail.com'

def get_event_list(calendar_id):
    page_token = None
    event_dict = {}
    while True:
        events = obj.service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in events['items']:
            if int(event["start"]["dateTime"].split('T')[0].split('-')[1]) >= int(str(datetime.date.today()).split('-')[1]):
                name_event = f'{event["summary"]} - {event["start"]["dateTime"].split("T")[0].split("-")[2]}-{event["start"]["dateTime"].split("T")[0].split("-")[1]}-{event["start"]["dateTime"].split("T")[0].split("-")[0]}'
                event_dict[name_event] = event['id']
        page_token = events.get('nextPageToken')

        if not page_token:
            break
    return event_dict

print(get_event_list(calendar_id=calendar_id))



#pprint.pprint(obj.get_calendar_list())
#obj.add_calendar(calendar_id='1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com')
#pprint.pprint(obj.get_calendar_list())