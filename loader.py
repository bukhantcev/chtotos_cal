from aiogram import Dispatcher, Bot
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
memory = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
#bot = Bot(token='6444845044:AAEjIWUe8ZFzQBTJLctja-XAsdD3rfb7d74')
dp = Dispatcher(bot, storage=memory)

