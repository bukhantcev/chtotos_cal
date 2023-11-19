import pprint
import pprint
from aiogram import Dispatcher

from delete_dot import delete_dot
from google_cal import GoogleCalendar
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ContentType, \
    ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, Contact
from keyboards_cal import cal_kb, create_day_table, kb_creat_event
from db_config import add_new_procedura, find_procedura, delete_procedura
from keyboards import kb_mainmenu, kb_stop
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne
from keyboards import kb_mainmenu, kb_back_to_uslugi, sert_kb
from text_uslugi import text_uslugi
from db_config import cursor, find_idproceduri, find_procedura, connect, add_new_klient, update_klient, find_name_procedure
from fsm import  NewItem, CalendarBt
from aiogram.dispatcher import  FSMContext
from klients import Klients
from master_id import master_id
from keyboards import contact_keyboard
from aiogram import types
from digits import  digits
from sertificat_list import sertificat_list


#ПУНКТ МЕНЮ ОБО МНЕ
@dp.callback_query_handler(text='obomne')
async def obomne(cb: CallbackQuery):
    await cb.answer('👌')
    id = cb.from_user.id
    await bot.send_message(chat_id=id, text= text_obomne, reply_markup= sert_kb)
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)

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
    await bot.delete_message(chat_id=cb.from_user.id,message_id=cb.message.message_id)





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
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


@dp.callback_query_handler(text='zapis', state=None)
async def zapros_phone(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id, text='Для связи с Вами мне потребуется номер Вашего '
                                                         'телефона. Чтобы поделиться контактом, нажмите кнопку ниже ⬇️.',
                           reply_markup=await contact_keyboard())
    await cb.answer('👌')
    await NewItem.phone.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)

@dp.message_handler(state=NewItem.phone, content_types=types.ContentType.CONTACT)
async def phone_catch(message: Message, state: FSMContext):
    contact = message.contact

    await state.update_data({'phone':contact})
    data = await state.get_data()
    new_data = (contact.phone_number, message.from_user.id)
    update_klient(new_data, 'phone')
    connect.commit()
    if find_name_procedure((message.from_user.id,)) != []:
        name_procedura = find_name_procedure((message.from_user.id,))[0][0]
        new_data1 = (name_procedura, message.from_user.id)
        update_klient(new_data1, 'procedure')
        connect.commit()
    await message.answer('Я работаю по будням с 15:30 до 21:00, сб - вс с 11:00 до 19:00. На какую дату Вы хотите записаться?',reply_markup=ReplyKeyboardRemove())
    await NewItem.date.set()



@dp.message_handler(state=NewItem.date)
async def phone_catch(message: Message, state: FSMContext):
    await state.update_data({'date':delete_dot(message.text)})
    data = await state.get_data()
    name_procedura = find_name_procedure((message.from_user.id,))
    if name_procedura != []:
        name_proc = 'Не выбрано' if name_procedura[0][0] == None else name_procedura[0][0]
    else:
        name_proc = 'Не выбрано'
    us_name = 'Нет' if message.from_user.username == None else f'@{message.from_user.username}'
    vizitka = await state.get_data('phone')
    await message.answer(text='Если эти дата и время свободны, Вам придет уведомление, в противном случае я свяжусь с вами для уточнения деталлей записи.')
    await bot.send_contact(chat_id=master_id, first_name=vizitka.get('phone').first_name, vcard=vizitka.get('phone').vcard, phone_number=vizitka.get('phone').phone_number)
    await bot.send_message(chat_id=master_id, text=f'Клиент {message.from_user.full_name} хочет записаться '
                                                   f'на процедуру:\n{name_proc}.\n\nПредпочтительная дата записи:'
                                                   f'\n{data.get("date")}. \n\nusername: {us_name}.\n'
                                                   f'\nТелефон: +{vizitka.get("phone").phone_number}.\n\n id клиента: {message.from_user.id}', reply_markup=kb_creat_event)
    await state.finish()


@dp.callback_query_handler(text='event_no')
async def otkaz(cb: CallbackQuery):
    await cb.answer('Запись отменена!!!')
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
    new_data = ('otmena', digits(cb.message.text.split('.')[4]))
    update_klient(new_data, 'status_recording')
    connect.commit()


@dp.callback_query_handler(text='event_yes', state=None)
async def calendar(cb: CallbackQuery):
    if cb.data == 'event_yes':
        await cb.answer('👌')
        await bot.send_message(chat_id=cb.from_user.id, text='Выбери месяц:', reply_markup=cal_kb)
        await CalendarBt.month.set()
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=None)
        print(digits(cb.message.text.split('.')[4]))
        new_data = ('in_work', digits(cb.message.text.split('.')[4]))
        update_klient(new_data, 'status_recording')
        connect.commit()



@dp.callback_query_handler(state=CalendarBt.month)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'month': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    print(data.get('month'))
    days_bt_text = create_day_table(int(data.get('month').split('-')[1]))
    days_kb = InlineKeyboardMarkup(row_width=7, inline_keyboard=days_bt_text)
    await bot.send_message(chat_id=cb.from_user.id, text=f'Выбран месяц: {data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                                         f'\nВыбери число:', reply_markup=days_kb)
    await CalendarBt.day.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


@dp.callback_query_handler(state=CalendarBt.day)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'day': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    print(data.get('day'))
    await bot.send_message(chat_id=cb.from_user.id, text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                                         f'\nВведи время:')
    await CalendarBt.time.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


@dp.message_handler(state=CalendarBt.time)
async def calendar_month(message: Message, state: FSMContext):
    content = str(message.text)

    if len(content) == 5 and content[2] == ':' and content.split(':')[0].isdigit() and 0 <= int(content.split(':')[0]) <=23 and content.split(':')[1].isdigit() and 0 <= int(content.split(':')[1]) <=59:

        await state.update_data({'time': message.text})
        data = await state.get_data()
        print(data.get('time'))
        await message.answer(text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}\nВремя: {data.get("time")}\nСоздать запись?',
                             reply_markup=kb_creat_event)
        await CalendarBt.final.set()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    else:
        await message.answer('Необходимо ввести время в формате чч:мм!')

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
        info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
        new_data = ('otmena', info[0][0])
        update_klient(new_data, 'status_recording')
        connect.commit()
    else:
        try:

            info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
            first_name = info[0][1]
            last_name = info[0][2] if info[0][2] != None else ''
            procedura = info[0][4] if info[0][4] != None else 'не выбрана'
            tg_id = info[0][3] if info[0][3] != None else 'нет'
            summary = f'{first_name} {last_name}'
            description = f'Процедура: {procedura}\n\nTG_id: {tg_id}\n\nТелефон: ' \
                          f'+{info[0][8]}'f'\n\nid клиента: {info[0][0]}'
            dateTime_start = f'{data.get("month")}-{data.get("day")}T{data.get("time")}:00+03:00'
            dateTime_end = f'{data.get("month")}-{data.get("day")}T{data.get("time")}:00+03:00'

            obj = GoogleCalendar()

            calendar_id = '1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com'

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
            print(event.get('id'))

            await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=None)
            await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                                text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                                     f'\nВремя: {data.get("time")}\nЗапись добавлена в календарь!')

            await bot.send_message(chat_id=cb.from_user.id, text=f'Вы записаны на {data.get("day")}-{data.get("month").split("-")[1]}'
                                                                 f'-{data.get("month").split("-")[0]}\n🕒: {data.get("time")}\n'
                                                                 f'Наш адрес и телефон Вы можете найти в разделе Контакты. Будем рады видеть Вас! ')
            new_data = ('active', info[0][0])
            update_klient(new_data, 'status_recording')
            connect.commit()


            await state.finish()
            await cb.answer('👌')
        except:
            await cb.answer('Что-то пошло не так!!!')



@dp.callback_query_handler(text='back_to_main_menu')
async def info(cb: CallbackQuery):
    await bot.edit_message_text(text='-------------ГЛАВНОЕ МЕНЮ-------------', chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=kb_mainmenu)

@dp.callback_query_handler(text='view_sertificates')
async def view_sertificate(cb: CallbackQuery):
    for i in range(len(sertificat_list)):
        path = f'sertificat_file/sert_{i+1}.jpg'
        file = InputFile(path)
        if i == len(sertificat_list)-1:
            await bot.send_photo(chat_id=cb.from_user.id, photo=file, reply_markup=kb_mainmenu)
        else:
            await bot.send_photo(chat_id=cb.from_user.id, photo=file)



@dp.callback_query_handler(text='raboti')
async def raboti(cb: CallbackQuery):
    await cb.answer('...Раздел находится в разработке...')


@dp.callback_query_handler(text='otzivi')
async def otzivi(cb: CallbackQuery):
    await cb.answer('...Раздел находится в разработке...')


@dp.callback_query_handler(text='kontakti')
async def kontakti(cb: CallbackQuery):
    await cb.answer('...Раздел находится в разработке...')





@dp.callback_query_handler()
async def print_commands(cb: CallbackQuery):
    command = cb.data
    if command.split('_')[0] == 'ukol':
        proceduri_id = find_idproceduri((command,))[0][0]
        descr = f'{find_procedura((proceduri_id,))[0][5]}\n\n🕒 {find_procedura((proceduri_id,))[0][2]}\n\n💰 {find_procedura((proceduri_id,))[0][3]}'
        photo = InputFile(f'foto_proceduri/{proceduri_id}.jpg')

        await bot.send_photo(chat_id=cb.message.chat.id, photo=photo, caption=descr, reply_markup=kb_back_to_uslugi)
        await cb.answer('👌')
        procedure = (find_procedura((proceduri_id,))[0][1])
        new_data = (procedure, cb.from_user.id)
        update_klient(new_data, 'last_procedure')
        connect.commit()
        await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)

'''async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text=("📱 Отправить"), request_contact=True)
    markup.add(first_button)
    return markup


# handlers.py
@dp.message_handler(commands=("contact"))
async def share_number(message: Message):
    await message.answer("Нажмите на кнопку ниже, чтобы отправить контакт", reply_markup=await contact_keyboard())

@dp.message_handler(content_types=ContentType.CONTACT)
async def get_contact(message: Message):
    contact = message.contact
    await bot.send_contact(chat_id=master_id, vcard=contact, phone_number=contact.phone_number, first_name=contact.first_name)
    await message.answer(f"Спасибо, {contact.full_name}.\n"
                         f"Ваш номер {contact.phone_number} был получен",
                         reply_markup=ReplyKeyboardRemove())
'''









