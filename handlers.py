from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions

from keyboards_cal import cal_kb
from db_config import add_new_procedura, find_procedura, delete_procedura, add_new_klient, update_klient, connect, cursor
from keyboards import kb_mainmenu
from klients import Klients
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne



@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(text_welcome, reply_markup=kb_mainmenu)
    klient = Klients(tg_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                     tg_username=message.from_user.username)
    tg_id = klient.tg_id
    first_name = klient.first_name
    last_name = klient.last_name
    tg_username = klient.tg_username
    new_klient = (tg_id, first_name, last_name, tg_username)
    add_new_klient(new_klient)
    print(message.from_user.id)
    cursor.execute('SELECT * FROM klients')
    data = cursor.fetchall()
    for i in range(len(data)):
        print(data[i])






@dp.message_handler(commands=['main_menu'], state='*')
async def info(message: Message, state: FSMContext):
    await state.finish()
    try:
        message_id = message.message_id
        while True:
            await bot.delete_message(message.chat.id, message_id)
            message_id = message_id-1
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

@dp.message_handler(content_types='photo')
async def photo(message: Message):
    print(message)

