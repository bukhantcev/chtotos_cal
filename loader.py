from aiogram import Dispatcher, Bot
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

memory = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
# bot = Bot(token='6283280993:AAHi8EqmQ41zE8rLl_0ayUexaX69DlCxs20')
dp = Dispatcher(bot, storage=memory)
