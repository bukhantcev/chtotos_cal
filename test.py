import pprint

from google_cal import GoogleCalendar


obj = GoogleCalendar()
pprint.pprint(obj.get_calendar_list())

calendar_id = 'bukhantcev@gmail.com'

event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2023-11-09T07:00:00+03:00',
  },
  'end': {
    'dateTime': '2023-11-09T17:00:00+03:00',
  }
}
event = obj.add_event(calendar_id=calendar_id, body=event)