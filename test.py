from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_cal import GoogleCalendar
obj = GoogleCalendar()

calendar_id = 'bukhantcev@gmail.com'
page_token = None
while True:
  events = obj.service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
  for event in events['items']:
    print (event)
  page_token = events.get('nextPageToken')
  if not page_token:
    break