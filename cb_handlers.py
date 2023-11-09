import pprint
import pprint
from google_cal import GoogleCalendar
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from keyboards_cal import cal_kb, create_day_table, kb_creat_event
from db_config import add_new_procedura, find_procedura, delete_procedura
from keyboards import kb_mainmenu
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne
from keyboards import kb_mainmenu, kb_back_to_uslugi
from text_uslugi import text_uslugi
from db_config import cursor, find_idproceduri, find_procedura, connect, add_new_klient, update_klient, find_name_procedure
from fsm import  NewItem, CalendarBt
from aiogram.dispatcher import  FSMContext
from klients import Klients
from master_id import master_id


#ПУНКТ МЕНЮ ОБО МНЕ
@dp.callback_query_handler(text='obomne')
async def obomne(cb: CallbackQuery):
    await cb.answer('👌')
    id = cb.from_user.id
    await bot.send_message(chat_id=id, text= text_obomne, reply_markup= kb_mainmenu)

#ПУНКТ МЕНЮ УСЛУГИ
@dp.callback_query_handler(text='uslugi')
async def uslugi(cb: CallbackQuery):
    await cb.answer('👌')
    cursor.execute('SELECT * FROM proceduri')
    list_button_uslugi = []
    for uslugi_bt in cursor.fetchall():
        list_button_uslugi.append([InlineKeyboardButton(text=str(uslugi_bt[1]), callback_data=str(uslugi_bt[4]))])
    kb_uslugi = InlineKeyboardMarkup(inline_keyboard=list_button_uslugi)
    id = cb.from_user.id
    await bot.send_message(chat_id=id, text=text_uslugi, reply_markup=kb_uslugi)





#ПУНКТ МЕНЮ УСЛУГИ
@dp.callback_query_handler(text='back_uslugi')
async def back_uslugi(cb: CallbackQuery):
    await cb.answer('👌')
    cursor.execute('SELECT * FROM proceduri')
    list_button_uslugi = []
    for uslugi_bt in cursor.fetchall():
        list_button_uslugi.append([InlineKeyboardButton(text=str(uslugi_bt[1]), callback_data=str(uslugi_bt[4]))])
    kb_uslugi = InlineKeyboardMarkup(inline_keyboard=list_button_uslugi)
    id = cb.from_user.id
    await bot.send_message(chat_id=id, text=text_uslugi, reply_markup=kb_uslugi)


@dp.callback_query_handler(text='zapis', state=None)
async def zapros_phone(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id, text='Для связи с Вами мне потребуется номер Вашего телефона. Отправьте его, пожалуйста, в ответном сообщении.')
    await cb.answer('👌')
    new_data = ('in_work', cb.from_user.id)
    update_klient(new_data, 'status_recording')
    connect.commit()
    await NewItem.phone.set()

@dp.message_handler(state=NewItem.phone)
async def phone_catch(message: Message, state: FSMContext):
    await state.update_data({'phone':message.text})
    data = await state.get_data()
    new_data = (data.get('phone'), message.from_user.id)
    update_klient(new_data, 'phone')
    if find_name_procedure((message.from_user.id,)) != []:
        name_procedura = find_name_procedure((message.from_user.id,))[0][0]
        new_data1 = (name_procedura, message.from_user.id)
        update_klient(new_data1, 'procedure')
    await message.answer('Я работаю по будням с 15:30 до 21:00, сб - вс с 11:00 до 19:00. На какую даты Вы хотите записаться?')
    await NewItem.date.set()



@dp.message_handler(state=NewItem.date)
async def phone_catch(message: Message, state: FSMContext):
    await state.update_data({'date':message.text})
    data = await state.get_data()
    name_procedura = find_name_procedure((message.from_user.id,))
    if name_procedura != []:
        name_proc = 'Не выбрано' if name_procedura[0][0] == None else name_procedura[0][0]
    else:
        name_proc = 'Не выбрано'
    us_name = 'Нет' if message.from_user.username == None else f'@{message.from_user.username}'
    await bot.send_message(chat_id=master_id, text=f'Клиент {message.from_user.full_name} хочет записаться '
                                                   f'на процедуру:\n{name_proc}\n\nПредпочтительная дата записи:'
                                                   f'\n{data.get("date")} \n\nid: {us_name}\n'
                                                   f'\nТелефон: {data.get("phone")}', reply_markup=kb_creat_event)
    await state.finish()


@dp.callback_query_handler(text='event_no')
async def otkaz(cb: CallbackQuery):
    await cb.answer('Запись отменена!!!')
    await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=None)


@dp.callback_query_handler(text='event_yes', state=None)
async def calendar(cb: CallbackQuery):
    if cb.data == 'event_yes':
        await cb.answer('👌')
        await bot.send_message(chat_id=cb.from_user.id, text='Выбери месяц:', reply_markup=cal_kb)
        await CalendarBt.month.set()



@dp.callback_query_handler(state=CalendarBt.month)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'month': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    print(data.get('month'))
    days_bt_text = create_day_table(int(data.get('month').split('-')[1]))
    days_kb = InlineKeyboardMarkup(row_width=7)
    days_kb = InlineKeyboardMarkup(inline_keyboard=days_bt_text)
    await bot.send_message(chat_id=cb.from_user.id, text=f'Выбран месяц: {data.get("month")}\nВыбери число:', reply_markup=days_kb)
    await CalendarBt.day.set()


@dp.callback_query_handler(state=CalendarBt.day)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'day': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    print(data.get('day'))
    await bot.send_message(chat_id=cb.from_user.id, text=f'Выбрана дата: {data.get("month")}-{data.get("day")}\nВведи время:')
    await CalendarBt.time.set()


@dp.message_handler(state=CalendarBt.time)
async def calendar_month(message: Message, state: FSMContext):
    await state.update_data({'time': message.text})
    data = await state.get_data()
    print(data.get('time'))
    await message.answer(text=f'Выбрана дата: {data.get("month")}-{data.get("day")}\nВремя: {data.get("time")}\nСоздать запись?',
                         reply_markup=kb_creat_event)
    await CalendarBt.final.set()

#Dobavlenie zapisi v calendar
@dp.callback_query_handler(state=CalendarBt.final)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'final': cb.data})
    data = await state.get_data()
    print(data.get('final'))
    if data.get('final') == 'event_no':
        await bot.send_message(chat_id=cb.from_user.id, text='Запись отменена!!!')
        await state.finish()
        await cb.answer('👌')
    else:
        info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
        summary = f'{info[0][1]} {info[0][2]}'
        description = f'Процедура: {info[0][4]}\n\nTG_id: {info[0][3]}\n\nТелефон: ' \
                      f'{info[0][8]}'f'\n\nid клиента: {info[0][0]}'
        dateTime_start = f'{data.get("month")}-{data.get("day")}T{data.get("time")}:00+03:00'
        dateTime_end = f'{data.get("month")}-{data.get("day")}T{data.get("time")}:00+03:00'

        obj = GoogleCalendar()
        pprint.pprint(obj.get_calendar_list())

        calendar_id = 'bukhantcev@gmail.com'

        event = {
            'summary': summary,
            'location': 'RAI BEAUTY SPACE',
            'description': description,
            'start': {
                'dateTime': dateTime_start,
            },
            'end': {
                'dateTime': dateTime_end,
            }
        }
        event = obj.add_event(calendar_id=calendar_id, body=event)

        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=None)
        await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            text=f'Выбрана дата: {data.get("month")}-{data.get("day")}\nВремя: {data.get("time")}\nЗапись добавлена в календарь!')

        await state.finish()
        await cb.answer('👌')


@dp.callback_query_handler()
async def print_commands(cb: CallbackQuery):
    command = cb.data
    proceduri_id = find_idproceduri((command,))[0][0]
    descr = f'{find_procedura((proceduri_id,))[0][5]}\n\n🕒 {find_procedura((proceduri_id,))[0][2]}\n\n💰 {find_procedura((proceduri_id,))[0][3]}'
    photo = InputFile(f'foto_proceduri/{proceduri_id}.jpg')

    await bot.send_photo(chat_id=cb.message.chat.id, photo=photo, caption=descr, reply_markup=kb_back_to_uslugi)
    await cb.answer('👌')
    procedure = (find_procedura((proceduri_id,))[0][1])
    new_data = (procedure, cb.from_user.id)
    update_klient(new_data, 'last_procedure')

@dp.message_handler(commands=['test'])
async def test(m: Message):
    cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"')









