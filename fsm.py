from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import dp
from aiogram.types import Message, CallbackQuery



class NewItem(StatesGroup):

    phone = State()
    date = State()

class CalendarBt(StatesGroup):

    user = State()
    month = State()
    day = State()
    time = State()
    final = State()



class PhotoSertificate(StatesGroup):


    photo_id = State()


