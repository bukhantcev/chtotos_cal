from aiogram.types import Message, CallbackQuery

from db_config import add_new_procedura, find_procedura, delete_procedura
from keyboards import kb_mainmenu
from loader import dp, bot, memory
from text_welcome import text_welcome
from text_obomne import text_obomne
from fsm import  NewItem
from aiogram.dispatcher import  FSMContext
from loader import memory


@dp.callback_query_handler(text='zapis', state=None)
async def zapros_phone(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id, text='Пришли номер')
    await NewItem.phone.set()

@dp.message_handler(state=NewItem.phone)
async def phone_catch(message: Message, state: FSMContext):
    await state.update_data(message.text)
    data = await state.get_data()
    print(data)
    await state.finish()