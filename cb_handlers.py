
import os
import pprint
import pprint
from datetime import datetime
from delete_foto import delete_foto
from aiogram import Dispatcher
from convert_to_int import convert_to_int, sort_actual_list
from delete_dot import delete_dot
from google_cal import GoogleCalendar, get_event_list
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ContentType, \
    ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, Contact, InputMediaPhoto, MediaGroup
from keyboards_cal import cal_kb, create_day_table, kb_creat_event
from db_config import add_new_procedura, find_procedura, delete_procedura
from keyboards import kb_mainmenu, kb_stop, kb_raboti, kb_back_raboti, kb_menu_solo, kb_raboti_admin
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne
from keyboards import kb_mainmenu, kb_back_to_uslugi, sert_kb, kb_sert_seredina, kb_sert_final, kb_sert_nachalo, kb_sert_final_del, kb_sert_nachalo_del, kb_sert_seredina_del
from text_uslugi import text_uslugi
from db_config import cursor, find_idproceduri, find_procedura, connect, add_new_klient, update_klient, \
    find_name_procedure, update_photo_sertificate
from fsm import NewItem, CalendarBt, Count, Raboti, PhotoSertificate
from aiogram.dispatcher import FSMContext
from klients import Klients
from master_id import master_id
from keyboards import contact_keyboard
from aiogram import types
from digits import digits
from sertificat_list import sertificat_list
from date_time import get_tomorow
import asyncio
from kontacts import text_kontacts
from date_time import get_today, future
from middleware.config import admin_id


# ПУНКТ МЕНЮ ОБО МНЕ
@dp.callback_query_handler(text='obomne')
async def obomne(cb: CallbackQuery):
    await cb.answer('👌')
    id = cb.from_user.id
    await bot.send_message(chat_id=id, text=text_obomne, reply_markup=sert_kb)
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


# ПУНКТ МЕНЮ УСЛУГИ
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
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


# ПУНКТ МЕНЮ УСЛУГИ ВОЗВРАТ
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


# ЗАПИСЬ НАЧАЛО
@dp.callback_query_handler(text='zapis', state=None)
async def zapros_phone(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id, text='Для связи с Вами мне потребуется номер Вашего '
                                                         'телефона. Чтобы поделиться контактом, нажмите кнопку ниже ⬇️.',
                           reply_markup=await contact_keyboard())
    await cb.answer('👌')
    await NewItem.phone.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


# ЗАПИСЬ НОМЕР ТЕЛЕФОНА
@dp.message_handler(state=NewItem.phone, content_types=types.ContentType.CONTACT)
async def phone_catch(message: Message, state: FSMContext):
    contact = message.contact

    await state.update_data({'phone': contact})
    data = await state.get_data()
    new_data = (contact.phone_number, message.from_user.id)
    update_klient(new_data, 'phone')
    connect.commit()
    if find_name_procedure((message.from_user.id,)) != []:
        name_procedura = find_name_procedure((message.from_user.id,))[0][0]
        new_data1 = (name_procedura, message.from_user.id)
        update_klient(new_data1, 'procedure')
        connect.commit()
    await message.answer(
        'Я работаю по будням с 15:30 до 21:00, сб - вс с 11:00 до 19:00. На какую дату Вы хотите записаться?',
        reply_markup=ReplyKeyboardRemove())
    await NewItem.date.set()
    klient = Klients(tg_id=message.from_user.id, first_name=message.from_user.first_name,
                     last_name=message.from_user.last_name,
                     tg_username=message.from_user.username)
    tg_id = klient.tg_id
    first_name = klient.first_name
    last_name = klient.last_name
    tg_username = klient.tg_username
    new_klient = (tg_id, first_name, last_name, tg_username)
    add_new_klient(new_klient)
    print(message.from_user.id)


# ЗАПИСЬ ЖЕЛАЕМАЯ ДАТА
@dp.message_handler(state=NewItem.date)
async def phone_catch(message: Message, state: FSMContext):
    await state.update_data({'date': delete_dot(message.text)})
    data = await state.get_data()
    name_procedura = find_name_procedure((message.from_user.id,))
    if name_procedura != []:
        name_proc = 'Не выбрано' if name_procedura[0][0] == None else name_procedura[0][0]
    else:
        name_proc = 'Не выбрано'
    us_name = 'Нет' if message.from_user.username == None else f'@{message.from_user.username}'
    vizitka = await state.get_data('phone')
    await message.answer(
        text='Если эти дата и время свободны, Вам придет уведомление, в противном случае я свяжусь с вами для уточнения деталлей записи.')
    await bot.send_contact(chat_id=master_id, first_name=vizitka.get('phone').first_name,
                           vcard=vizitka.get('phone').vcard, phone_number=vizitka.get('phone').phone_number)
    await bot.send_message(chat_id=master_id, text=f'Клиент {message.from_user.full_name} хочет записаться '
                                                   f'на процедуру:\n{name_proc}.\n\nПредпочтительная дата записи:'
                                                   f'\n{data.get("date")}. \n\nusername: {us_name}.\n'
                                                   f'\nТелефон: +{vizitka.get("phone").phone_number}.\n\n id клиента: {message.from_user.id}',
                           reply_markup=kb_creat_event)
    await state.finish()


# ЗАПИСЬ ОТМЕНА
@dp.callback_query_handler(text='event_no')
async def otkaz(cb: CallbackQuery):
    await cb.answer('Запись отменена!!!')
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
    new_data = ('otmena', digits(cb.message.text.split('.')[4]))
    update_klient(new_data, 'status_recording')
    connect.commit()


# ЗАПИСЬ ПОДТВЕРЖДЕНИЕ
@dp.callback_query_handler(text='event_yes', state=None)
async def calendar(cb: CallbackQuery):
    if cb.data == 'event_yes':
        await cb.answer('👌')
        await bot.send_message(chat_id=cb.from_user.id, text='Выбери месяц:', reply_markup=cal_kb)
        await CalendarBt.month.set()
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=None)
        new_data = ('in_work', digits(cb.message.text.split('.')[4]))
        update_klient(new_data, 'status_recording')
        connect.commit()


# КАЛЕНДАРЬ МЕСЯЦ И ГОД
@dp.callback_query_handler(state=CalendarBt.month)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'month': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    days_bt_text = create_day_table(int(data.get('month').split('-')[1]))
    days_kb = InlineKeyboardMarkup(row_width=7, inline_keyboard=days_bt_text)
    await bot.send_message(chat_id=cb.from_user.id,
                           text=f'Выбран месяц: {data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                f'\nВыбери число:', reply_markup=days_kb)
    await CalendarBt.day.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


# КАЛЕНДАРЬ ДЕНЬ
@dp.callback_query_handler(state=CalendarBt.day)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'day': cb.data})
    await cb.answer('👌')
    data = await state.get_data()
    await bot.send_message(chat_id=cb.from_user.id,
                           text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                f'\nВведи время:')
    await CalendarBt.time.set()
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


# КАЛЕНДАРЬ ВРЕМЯ
@dp.message_handler(state=CalendarBt.time)
async def calendar_month(message: Message, state: FSMContext):
    content = str(message.text)

    if len(content) == 5 and content[2] == ':' and content.split(':')[0].isdigit() and 0 <= int(
            content.split(':')[0]) <= 23 and content.split(':')[1].isdigit() and 0 <= int(content.split(':')[1]) <= 59:

        await state.update_data({'time': message.text})
        data = await state.get_data()
        await message.answer(
            text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}\nВремя: {data.get("time")}\nСоздать запись?',
            reply_markup=kb_creat_event)
        await CalendarBt.final.set()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    else:
        await message.answer('Необходимо ввести время в формате чч:мм!')


# Dobavlenie zapisi v calendar
@dp.callback_query_handler(state=CalendarBt.final)
async def calendar_month(cb: CallbackQuery, state: FSMContext):
    await state.update_data({'final': cb.data})
    data = await state.get_data()
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

            await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                                reply_markup=None)
            await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                        text=f'Выбрана дата: {data.get("day")}-{data.get("month").split("-")[1]}-{data.get("month").split("-")[0]}'
                                             f'\nВремя: {data.get("time")}\nЗапись добавлена в календарь!')

            await bot.send_message(chat_id=info[0][0],
                                   text=f'Вы записаны на {data.get("day")}-{data.get("month").split("-")[1]}'
                                        f'-{data.get("month").split("-")[0]}\n🕒: {data.get("time")}\n'
                                        f'Наш адрес и телефон Вы можете найти в разделе Контакты. Будем рады видеть Вас! ')
            new_data = ('active', info[0][0])
            update_klient(new_data, 'status_recording')
            connect.commit()

            await state.finish()
            await cb.answer('👌')
        except:
            await cb.answer('Что-то пошло не так!!!')
            await state.finish()


# ВОЗВРАТ В ГЛАВНОЕ МЕНЮ
@dp.callback_query_handler(text='back_to_main_menu')
async def info(cb: CallbackQuery):
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    await bot.send_message(text='-------------ГЛАВНОЕ МЕНЮ-------------', chat_id=cb.from_user.id, reply_markup=kb_mainmenu)


# ПОКАЗАТЬ СЕРТИФИКАТЫ
@dp.callback_query_handler(text='view_sertificates', state=None)
async def view_sertificate(cb: CallbackQuery, state: FSMContext):
    path_dir = 'sertificat_file'
    list_photo = os.listdir(path_dir)
    path = f'sertificat_file/{list_photo[0]}'
    file = InputFile(path)
    await cb.answer('👌')
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    await bot.send_photo(chat_id=cb.from_user.id, photo=file, reply_markup=kb_sert_nachalo)
    await Count.next_count.set()


# СЕРТИФИКАТЫ ВПЕРЕД/НАЗАД/ВЫХОД
@dp.callback_query_handler(text=['go_forward', 'go_back', 'vozvrat_obo_mne', 'button_clear', 'del_sert'], state=Count.next_count)
async def view_sertificate(cb: CallbackQuery, state: FSMContext):
    start_state = await state.get_data()
    if start_state.get('next_count') == None:
        await state.update_data({'next_count':os.listdir('sertificat_file')[0]})
    start_state = await state.get_data()
    file_index = int(str(start_state.get('next_count')).split('_')[1].split('.')[0])
    if cb.data == 'go_forward':
        file_index += 1
        await cb.answer('👌')
        if file_index == 1:
            kb = kb_sert_nachalo_del if cb.from_user.id in admin_id else kb_sert_nachalo

        elif file_index == len(os.listdir('sertificat_file')):
            kb = kb_sert_final_del if cb.from_user.id in admin_id else kb_sert_final
        else:
            kb = kb_sert_seredina_del if cb.from_user.id in admin_id else kb_sert_seredina
        if file_index <= len(os.listdir('sertificat_file'))+1:
            path = (f"sertificat_file/sert_{file_index}.jpg")
            with open(path, 'rb') as file:
                try:
                    photo = InputMediaPhoto(file, caption=f'sert_{file_index}.jpg' if cb.from_user.id in admin_id else None)
                    await bot.edit_message_media(chat_id=cb.message.chat.id, message_id=cb.message.message_id,
                                                 media=photo,
                                                 reply_markup=kb)
                    await state.update_data({'next_count': f'sert_{file_index}.jpg'})

                except:
                    pass
    if cb.data == 'go_back':
        await cb.answer('👌')
        file_index -= 1
        if file_index == 1:
            kb = kb_sert_nachalo_del if cb.from_user.id in admin_id else kb_sert_nachalo
        elif file_index == len(os.listdir('sertificat_file')):
            kb = kb_sert_final_del if cb.from_user.id in admin_id else kb_sert_final
        else:
            kb = kb_sert_seredina_del if cb.from_user.id in admin_id else kb_sert_seredina
        if file_index >= 1:
            path = (f"sertificat_file/sert_{file_index}.jpg")
            with open(path, 'rb') as file:
                try:
                    photo = InputMediaPhoto(file, caption=f'sert_{file_index}.jpg' if cb.from_user.id in admin_id else None)
                    await bot.edit_message_media(chat_id=cb.message.chat.id, message_id=cb.message.message_id,
                                                 media=photo,
                                                 reply_markup=kb)
                    await state.update_data({'next_count': f'sert_{file_index}.jpg'})

                except:
                    pass
    if cb.data == 'vozvrat_obo_mne':
        await cb.answer('👌')
        await state.finish()
        await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
        await bot.send_message(text='-------------ГЛАВНОЕ МЕНЮ-------------', chat_id=cb.from_user.id,
                               reply_markup=kb_mainmenu)
    if cb.data == 'button_clear':
        await cb.answer('👌')
    if cb.data == 'del_sert':
        await cb.answer(text='Скопируй название файла и отправь его боту!', show_alert=True)


@dp.message_handler(state=Count.next_count)
async def delete_final(message:Message, state:FSMContext):
    if message.from_user.id in admin_id:
        try:
            if message.text in os.listdir('sertificat_file'):
                print(delete_foto(f"sertificat_file/{message.text}"))
                await message.answer("Фото удалено")
        except:
            print('Не удалось!')



@dp.callback_query_handler(text='raboti', state=None)
async def raboti(cb: CallbackQuery, state:FSMContext):
    await cb.answer('👌')
    try:
        count = 1
        while True:
            await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id-count)
            count += 1
    except:
        await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    await bot.send_message(chat_id=cb.from_user.id, text='--------Выберите раздел:--------', reply_markup=kb_raboti)
    await Raboti.raboti_state.set()

@dp.callback_query_handler(text='raboti', state=Raboti.raboti_state)
async def raboti(cb: CallbackQuery, state:FSMContext):
    await cb.answer('👌')
    try:
        count = 1
        while True:
            await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id-count)
            count += 1
    except:
        await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
        await bot.send_message(chat_id=cb.from_user.id, text='--------Выберите раздел:--------', reply_markup=kb_raboti)


@dp.callback_query_handler(text=os.listdir('raboti'), state=Raboti.raboti_state)
async def view_raboti(cb:CallbackQuery, state:FSMContext):
    await state.update_data({'raboti_state': cb.data})
    path_dir = f'raboti/{cb.data}'
    media = MediaGroup()
    kb = kb_raboti_admin if cb.from_user.id in admin_id else kb_back_raboti
    if len(os.listdir(path_dir)) > 0:
        if len(os.listdir(path_dir)) > 1:
            for file in os.listdir(path_dir):
                await state.update_data({'raboti_state': path_dir})
                media.attach_photo(photo=InputFile(f'{path_dir}/{file}'), caption=file if cb.from_user.id in admin_id else None) if file.split('.')[1] == 'jpg' else \
                    media.attach_video(video=InputFile(f'{path_dir}/{file}'), caption=file if cb.from_user.id in admin_id else None)
            await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
            await cb.answer(text='Загружаю файл.....')

            await bot.send_media_group(chat_id=cb.from_user.id, media=media)
            await bot.send_message(chat_id=cb.from_user.id, text=cb.data, reply_markup=kb)
        else:
            for file in os.listdir(path_dir):
                await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
                await cb.answer(text='Загружаю файл.....')
                await bot.send_photo(chat_id=cb.from_user.id, photo=InputFile(f'{path_dir}/{file}'), caption=file if cb.from_user.id in admin_id else None) if file.split('.')[1] == 'jpg' else await bot.send_video(chat_id=cb.from_user.id, video=InputFile(f'{path_dir}/{file}'), caption=file if cb.from_user.id in admin_id else None)
                await bot.send_message(chat_id=cb.from_user.id, text=cb.data, reply_markup=kb)

@dp.message_handler(content_types=['photo', 'video'], state=Raboti.raboti_state)
async def add_photo_raboti(message:Message, state:FSMContext):
    try:
        if message.from_user.id in admin_id:
            data = await state.get_data()
            try:
                name = str(data.get('raboti_state')).split('/')[1]
            except:
                name = data.get('raboti_state')

            if len(os.listdir(f'raboti/{name}')) < 10:
                if 'photo' in message:
                    await message.photo[-1].download(destination_file=f'raboti/{name}/'
                                                                      f'{str(os.listdir(f"raboti/{name}")[0]).split("_")[0]}_'
                                                                      f'{len(os.listdir(f"raboti/{name}"))+1}.jpg')
                if 'video' in message:
                    await message.video.download(destination_file=f'raboti/{name}/'
                                                                      f'{str(os.listdir(f"raboti/{name}")[0]).split("_")[0]}_'
                                                                      f'{len(os.listdir(f"raboti/{name}")) + 1}.mp4')

                await message.answer(f"Файл добавлен в папку {name}")
            else:
                await message.answer('Максимальное количество файлов - 10, придется что-то удалить((')

    except:
        await message.answer('Что-то пошло не так!')

@dp.callback_query_handler(text=['add_file_raboti', 'delete_file_raboti'], state=Raboti.raboti_state)
async def admin_raboti(cb:CallbackQuery, state:FSMContext):
    if cb.data == 'add_file_raboti':
        await cb.answer(text='Отравь фото или видео боту!', show_alert=True)
    if cb.data == 'delete_file_raboti':
        await cb.answer(text='Отправь сообщение Удалить (название файла). Название файла можно скопировать.', show_alert=True)


@dp.message_handler(state=Raboti.raboti_state)
async def delete_file(message:Message, state:FSMContext):
    if message.from_user.id in admin_id:
        data = await state.get_data()
        try:
            if 'удалить ' in message.text.lower():

                delete_foto(f'{data["raboti_state"]}/{message.text.split(" ")[1]}')
                await bot.send_message(chat_id=message.from_user.id, text='Файл удален!!!')
        except:
            await bot.send_message(chat_id=message.from_user.id, text='Файл не удален!!! Попробуй еще раз!')


@dp.callback_query_handler(text='otzivi')
async def otzivi(cb: CallbackQuery):
    await cb.answer('...Раздел находится в разработке...')


@dp.callback_query_handler(text='kontakti')
async def kontakti(cb: CallbackQuery):
    await cb.answer('👌')
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)
    await bot.send_location(chat_id=cb.message.chat.id, latitude=55.909554, longitude=38.050749)
    await bot.send_message(chat_id=cb.message.chat.id, text=text_kontacts, reply_markup=kb_menu_solo)


#ПОЛУЧЕНИЕ СПИСКА АКТИВНЫХ ЗАПИСЕЙ
@dp.callback_query_handler(text='get_event_list')
async def get_events(cb: CallbackQuery):
    try:
        await cb.answer('👌')
        calendar_id = '1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com'
        event_list = get_event_list(calendar_id=calendar_id)
        today_date = get_today()
        obj = GoogleCalendar()
        index = 0
        list_int = []
        actual_list = []
        for event in event_list:
            event_date = event.split(' - ')[1]
            if future(event_date):

                list_int.append(convert_to_int(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))))
                actual_list.append(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event)))


                index = 1
        if index == 0:
            await bot.send_message(chat_id=admin_id[1], text='Записей нет.')
            await bot.send_message(chat_id=admin_id[0], text='Записей нет.')

        if index == 1:
            sort_list = sorted(list_int)
            final_list = sort_actual_list(actual_list=actual_list, sort_list=sort_list)
            for eve in final_list:
                event_date = f"{str(obj.get_event(calendar_id=calendar_id, event_id=eve.get('id'))['start']['dateTime']).split('T')[0].split('-')[2]}-" \
                             f"{str(obj.get_event(calendar_id=calendar_id, event_id=eve.get('id'))['start']['dateTime']).split('T')[0].split('-')[1]}-" \
                             f"{str(obj.get_event(calendar_id=calendar_id, event_id=eve.get('id'))['start']['dateTime']).split('T')[0].split('-')[0]}"
                name = obj.get_event(calendar_id=calendar_id, event_id=eve.get("id"))['summary']
                procedura = \
                     str(obj.get_event(calendar_id=calendar_id, event_id=eve.get("id"))['description']).split(
                         'Процедура: ')[1].split('\n')[0]
                time_event = f"{str(obj.get_event(calendar_id=calendar_id, event_id=eve.get('id'))['start']['dateTime']).split('T')[1].split(':')[0]}:" \
                             f"{str(obj.get_event(calendar_id=calendar_id, event_id=eve.get('id'))['start']['dateTime']).split('T')[1].split(':')[1]}"
                await bot.send_message(chat_id=admin_id[1],
                                      text=f'{event_date}\n{name}\n{time_event}')
                await bot.send_message(chat_id=admin_id[0],
                                       text=f'{event_date}\n{name}\n{procedura}\n{time_event}')

    except:
        await bot.send_message(chat_id=admin_id[1], text='Проверка календаря не выполнена')
        await bot.send_message(chat_id=admin_id[0], text='Проверка календаря не выполнена')








# УСЛУГИ ВСЕГДА НА ПОСЛЕДНЕМ МЕСТЕ!!!
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
