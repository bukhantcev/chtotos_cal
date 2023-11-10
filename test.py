# keyboards.py
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text=_("📱 Отправить"), request_contact=True)
    markup.add(first_button)
    return markup


# handlers.py
@dp.message_handler(сommand=("contact"))
async def share_number(message: types.Message):
    await message.answer("Нажмите на кнопку ниже, чтобы отправить контакт", reply_markup=await contact_keyboard())

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    contact = message.contact
    await message.answer(f"Спасибо, {contact.full_name}.\n"
                         f"Ваш номер {contact.phone_number} был получен",
                         reply_markup=ReplyKeyboardRemove())

