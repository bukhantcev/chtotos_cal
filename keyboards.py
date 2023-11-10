from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButtonRequestUser


#Обычные кнопки:




# Инлайн кнопки:
#Main menu
list_buttonmenu = [
[InlineKeyboardButton(text='Обо мне', callback_data='obomne'),
InlineKeyboardButton(text='Услуги', callback_data='uslugi')],
[InlineKeyboardButton(text='Мои работы', callback_data='raboti'),
InlineKeyboardButton(text='Записаться', callback_data='zapis')],
[InlineKeyboardButton(text='Отзывы', callback_data='otzivi'),
InlineKeyboardButton(text='Контакты', callback_data='kontakti')]
]
kb_mainmenu = InlineKeyboardMarkup(inline_keyboard=list_buttonmenu)

bt_back_to_uslugi = InlineKeyboardButton(text='--Вернуться к услугам--', callback_data='back_uslugi')
bt_zapis = InlineKeyboardButton(text='--Записаться--', callback_data='zapis')
kb_back_to_uslugi = InlineKeyboardMarkup(row_width=1,)

kb_back_to_uslugi.row(bt_zapis)
kb_back_to_uslugi.row(bt_back_to_uslugi)

bt_stop = KeyboardButton(text='Отменить и выйти')
kb_stop = ReplyKeyboardMarkup([[bt_stop]], resize_keyboard=True)

async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text=("📱 Отправить"), request_contact=True)
    markup.add(first_button)
    return markup


