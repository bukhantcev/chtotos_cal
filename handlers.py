from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions
from fsm import PhotoSertificate
from keyboards_cal import cal_kb
from db_config import add_new_procedura, find_procedura, delete_procedura, add_new_klient, update_klient, connect, cursor, add_new_sert
from keyboards import kb_mainmenu
from klients import Klients
from loader import dp, bot
from text_welcome import text_welcome
from text_obomne import text_obomne



@dp.message_handler(commands=['start'])
async def start(message: Message, admin: bool):
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
    cursor.execute('SELECT * FROM photo_sertificate')
    data = cursor.fetchall()

    print(data)
    if admin:
        await message.answer('Привет админ!')







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

@dp.message_handler(commands=['add_sert'], state=None)
async def add_photo_sert(message: Message, state: FSMContext):
    await message.answer('Пришли фото по одной, у последней добавь описание "Стоп". Также можно написать "Стоп" в сообщении.')
    await PhotoSertificate.photo_id.set()
    
@dp.message_handler(content_types='photo', state=PhotoSertificate.photo_id)
async def get_photo_sert(message: Message, admin: bool, state: FSMContext):
    if admin:
        date = cursor.execute('SELECT * FROM photo_sertificate').fetchall()
        print(message.caption)
        if message.caption != 'Стоп':
            if len(date)==0:
                name = 'sert_1'
                photo_id = dict(message.photo[0]).get('file_id')
                new_sert = (name, photo_id)
                add_new_sert(new_sert=new_sert)
                await PhotoSertificate.photo_id.set()
                print(len(date))
            else:
                name = f"sert_{int(date[len(date)-1][1].split('_')[1]) + 1}"
                photo_id = dict(message.photo[0]).get('file_id')
                new_sert = (name, photo_id)
                add_new_sert(new_sert=new_sert)
                await PhotoSertificate.photo_id.set()
        else:
            await state.finish()
            await message.answer('Фото добавлены!')

@dp.message_handler(state=PhotoSertificate.photo_id)
async def error(message: Message, state: FSMContext):
    if message.text != 'Стоп':
        await message.answer('Пришли фото по одной, у последней добавь описание "Стоп". Также можно написать "Стоп" в сообщении.')
        await PhotoSertificate.photo_id.set()
    else:
        await message.answer('Закончили упражнение!')
        await state.finish()






