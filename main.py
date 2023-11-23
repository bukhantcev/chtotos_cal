import asyncio
from aiogram.types import Message
from aiogram.utils import executor
from db_config import create_table, create_table_klients, create_table_photo_sertificate
from loader import bot, dp
from handlers import dp
from cb_handlers import dp, go_napominanie
from admin import dp
from fill_db_proceduri import fill_db
from FM_handlers import dp
import middleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import napominanie
from datetime import datetime, timedelta


async def on_start(_):
    try:
        create_table()
        fill_db()
        create_table_klients()
        create_table_photo_sertificate()

        print('DB connection... OK')
    except:
        print('DB connection... Failure!!!')
    print('Bot run!')
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(napominanie.loop_message, trigger='cron', hour='11', minute='00', start_date=datetime.now(),
                      kwargs={'bt': bot})
    scheduler.start()


if __name__ == '__main__':
    middleware.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
