from loader import bot
from google_cal import get_event_list, GoogleCalendar
from date_time import get_tomorow





async def loop_message(bt:bot):
    try:
        calendar_id = '1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com'
        event_list = get_event_list(calendar_id=calendar_id)
        tomorrow_date = get_tomorow()
        obj = GoogleCalendar()
        for event in event_list:
            event_date = event.split(' - ')[1]
            if event_date == tomorrow_date:
                name = obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['summary']
                procedura = str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['description']).split('Процедура: ')[1].split('\n')[0]
                tg_id = str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['description']).split('id клиента: ')[1]
                time_event = f"{str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['start']['dateTime']).split('T')[1].split(':')[0]}:" \
                             f"{str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['start']['dateTime']).split('T')[1].split(':')[1]}"
                await bt.send_message(text=f'Здравствуйте, {name}! Напоминаем, что завтра Вы записаны на процедуру: {procedura}.'
                                            f'\n\nВремя записи - {time_event}\n\nАдрес:-----\nТелефон для связи:----- ', chat_id=tg_id)
                await bt.send_message(chat_id=admin_id[0], text=f'На завтра есть запись: {name}.\nПроцедура: {procedura}.\nВремя: {time_event}.')
            else:
                await bt.send_message(chat_id=admin_id[0], text='На завтра записей нет.')
        print('rabotaet')
    except:
        await bt.send_message(chat_id=admin_id[0], text='Проверка календаря не выполнена')