import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputMedia, InputFile, InputMediaPhoto
from aiogram.utils import exceptions

from date_time import get_tomorow, get_today
from google_cal import GoogleCalendar, get_event_list
from fsm import PhotoSertificate
from keyboards_cal import cal_kb
from db_config import add_new_procedura, find_procedura, delete_procedura, add_new_klient, update_klient, connect, \
    cursor, add_new_sert
from keyboards import kb_mainmenu, kb_get_event_list, kb_main
from klients import Klients
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne
import asyncio
from middleware.config import admin_id


# СТАРТ
@dp.message_handler(commands=['start'])
async def start(message: Message, admin: bool):
    path = 'start_photo/start_1.jpg'
    photo = InputFile(path)
    await message.answer_photo(caption=text_welcome, photo=photo, reply_markup=kb_mainmenu)
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
    cursor.execute('SELECT * FROM photo_sertificate')
    data = cursor.fetchall()


# ГЛАВНОЕ МЕНЮ
@dp.message_handler(commands=['main_menu'], state='*')
async def info(message: Message, state: FSMContext):
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
    await state.finish()
    try:
        message_id = message.message_id
        while True:
            await bot.delete_message(message.chat.id, message_id)
            message_id = message_id - 1
    except:
        pass

    await message.answer(text='-------------ГЛАВНОЕ МЕНЮ-------------', reply_markup=kb_mainmenu)

    new_data = (None, message.from_user.id)
    update_klient(new_data, 'last_procedure')
    try:
        info = cursor.execute('SELECT * FROM klients WHERE status_recording="in_work"').fetchall()
        new_data = ('otmena', info[0][0])
        update_klient(new_data, 'status_recording')
    except:
        print('ok')


# ДОБАВИТЬ СЕРТИФИКАТ
@dp.callback_query_handler(text='add_sert', state=None)
async def add_photo_sert(cb: CallbackQuery ,state: FSMContext):
    await cb.answer('👌')
    await bot.send_message(text=
        'Пришли фото по одной, у последней добавь описание "Стоп". Также можно написать "Стоп" в сообщении.', chat_id=cb.from_user.id)
    await PhotoSertificate.photo_id.set()


@dp.message_handler(content_types='photo', state=PhotoSertificate.photo_id)
async def get_photo_sert(message: Message, admin: bool, state: FSMContext):
    if admin:
        date = os.listdir('sertificat_file')
        if len(date) != 0:
            print(date)

            for file in date:
                file_index = int(file.split('_')[1].split('.')[0])
                os.rename(f'sertificat_file/{file}', f'sertificat_file/new_{file_index}.jpg')
            new_date = os.listdir('sertificat_file')
            for file in new_date:
                file_index = int(file.split('_')[1].split('.')[0])
                os.rename(f'sertificat_file/{file}', f'sertificat_file/sert_{file_index+1}.jpg')

        await message.photo[-1].download(destination_file='sertificat_file/sert_1.jpg')
        await PhotoSertificate.photo_id.set()
        await message.answer('Фото добавлено!')


@dp.message_handler(state=PhotoSertificate.photo_id)
async def error(message: Message, state: FSMContext):
    if message.text != 'Стоп':
        await message.answer(
            'Пришли фото по одной. Когда закончишь, напиши слово "Стоп"')
        await PhotoSertificate.photo_id.set()
    else:
        await message.answer('Закончили упражнение!')
        await state.finish()


@dp.message_handler(commands=['admin'])
async def get_event_l(message: Message, admin: bool):
    if admin:
        await message.answer(text='Пока так', reply_markup=kb_get_event_list)


@dp.message_handler(commands=['today'])
async def go_napominanie(message: Message, admin: bool):
    if admin:
        calendar_id = '1dbae5a038d3414d565f0e8ba342c1fa018ceb2d3d5bd0245ec6f610b978a446@group.calendar.google.com'
        event_list = get_event_list(calendar_id=calendar_id)
        today_date = get_today()
        obj = GoogleCalendar()
        index = 0
        for event in event_list:
            event_date = event.split(' - ')[1]
            if event_date == today_date:
                name = obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['summary']
                procedura = \
                    str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['description']).split(
                        'Процедура: ')[1].split('\n')[0]
                tg_id = \
                    str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['description']).split(
                        'id клиента: ')[1]
                time_event = f"{str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['start']['dateTime']).split('T')[1].split(':')[0]}:" \
                             f"{str(obj.get_event(calendar_id=calendar_id, event_id=event_list.get(event))['start']['dateTime']).split('T')[1].split(':')[1]}"
                await bot.send_message(
                    text=f'Здравствуйте, {str(name).split(" ")[0] if " " in str(name) else name}! Напоминаем, что сегодня {today_date} Вы записаны на процедуру: {procedura}.'
                         f'\n\nВремя записи - {time_event}\n\nАдрес: г. Щёлково, микрорайон Потаповский, д.1, к.1, BeautySpace RAI\nТелефон для связи: +7(916)-261-43-01 ', chat_id=tg_id)
                await bot.send_message(chat_id=admin_id[0],
                                       text=f'На сегодня есть запись: {name}.\nПроцедура: {procedura}.\nВремя: {time_event}.')
                await bot.send_message(chat_id=admin_id[1],
                                       text=f'На сегодня есть запись: {name}.\nПроцедура: {procedura}.\nВремя: {time_event}.')
                index = 1

        if index == 0:
            await bot.send_message(chat_id=admin_id[1], text='На сегодня записей нет.')
            await bot.send_message(chat_id=admin_id[0], text='На сегодня записей нет.')
