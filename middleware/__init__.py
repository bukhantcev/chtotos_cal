from aiogram import Dispatcher
from .middleware import Administrator

def setup(dp: Dispatcher):
    dp.middleware.setup(Administrator())