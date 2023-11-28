import pprint


def convert_to_int(event:dict):
    result = str(event['start']['dateTime']).split('T')[0].split('-')[0]+\
             str(event['start']['dateTime']).split('T')[0].split('-')[1]+\
             str(event['start']['dateTime']).split('T')[0].split('-')[2]+\
             str(event['start']['dateTime']).split('T')[1].split(':')[0]+\
             str(event['start']['dateTime']).split('T')[1].split(':')[1]
    result = int(result)

    return result


def sort_actual_list(actual_list: list, sort_list: list):
    result = []
    for i in range(len(sort_list)):
        for j in range(len(actual_list)):
            if sort_list[i] == convert_to_int(actual_list[j]):
                result.append(actual_list[j])
    return result



#convert_to_int({'kind': 'calendar#event', 'etag': '"3401983188936000"', 'id': 'qcn504fddd10uc3hr7g9tghrec', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cWNuNTA0ZmRkZDEwdWMzaHI3Zzl0Z2hyZWMgMWRiYWU1YTAzOGQzNDE0ZDU2NWYwZThiYTM0MmMxZmEwMThjZWIyZDNkNWJkMDI0NWVjNmY2MTBiOTc4YTQ0NkBn', 'created': '2023-11-26T09:39:54.000Z', 'updated': '2023-11-26T09:39:54.468Z', 'summary': 'Keithaera ', 'description': 'Процедура: не выбрана\n\nTG_id: keithaera\n\nТелефон: +79680356212\n\nid клиента: 1738054010', 'location': 'RAI BEAUTY SPACE', 'creator': {'email': 'calendar@studied-jigsaw-404516.iam.gserviceaccount.com'}, 'organizer': {'email': '1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com', 'displayName': 'BeautySpace', 'self': True}, 'start': {'dateTime': '2023-12-01T19:30:00+03:00', 'timeZone': 'UTC'}, 'end': {'dateTime': '2023-12-01T19:30:00+03:00', 'timeZone': 'UTC'}, 'iCalUID': 'qcn504fddd10uc3hr7g9tghrec@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'})