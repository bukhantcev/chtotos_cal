import os

from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    KeyboardButtonRequestUser

# Обычные кнопки:


# Инлайн кнопки:
# Main menu
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
kb_back_to_uslugi = InlineKeyboardMarkup(row_width=1, )

kb_back_to_uslugi.row(bt_zapis)
kb_back_to_uslugi.row(bt_back_to_uslugi)

bt_stop = KeyboardButton(text='Отменить и выйти')
kb_stop = ReplyKeyboardMarkup([[bt_stop]], resize_keyboard=True)


async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text=("📱 Отправить номер телефона"), request_contact=True)
    markup.add(first_button)
    return markup


sert_bt = InlineKeyboardButton(text='Посмотреть сертификаты', callback_data='view_sertificates')
back_to_main_menu = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back_to_main_menu')
sert_kb = InlineKeyboardMarkup(row_width=1)
sert_kb.row(sert_bt)
sert_kb.row(back_to_main_menu)

button_forward = InlineKeyboardButton(text='>>>', callback_data='go_forward')
button_back = InlineKeyboardButton(text='<<<', callback_data='go_back')
button_vozvrat_obo_mne = InlineKeyboardButton(text='-----Вернуться назад-----', callback_data='vozvrat_obo_mne')
button_clear = InlineKeyboardButton(text=' ', callback_data='button_clear')
button_del = InlineKeyboardButton(text='Удалить сертификат', callback_data='del_sert')
button_set_nachalo = [
    [button_clear, button_forward],
    [button_vozvrat_obo_mne]
]
button_set_seredina = [
    [button_back, button_forward],
    [button_vozvrat_obo_mne]
]
button_set_final = [
    [button_back, button_clear],
    [button_vozvrat_obo_mne]
]
button_set_final_del = [
    [button_back, button_clear],
    [button_vozvrat_obo_mne],
    [button_del]
]
button_set_seredina_del = [
    [button_back, button_forward],
    [button_vozvrat_obo_mne],
    [button_del]
]
button_set_nachalo_del = [
    [button_clear, button_forward],
    [button_vozvrat_obo_mne],
    [button_del]
]


kb_sert_nachalo = InlineKeyboardMarkup(inline_keyboard=button_set_nachalo)
kb_sert_seredina = InlineKeyboardMarkup(inline_keyboard=button_set_seredina)
kb_sert_final = InlineKeyboardMarkup(inline_keyboard=button_set_final)
kb_sert_nachalo_del = InlineKeyboardMarkup(inline_keyboard=button_set_nachalo_del)
kb_sert_seredina_del = InlineKeyboardMarkup(inline_keyboard=button_set_seredina_del)
kb_sert_final_del = InlineKeyboardMarkup(inline_keyboard=button_set_final_del)

bt_stop_foto = KeyboardButton(text='Стоп')
kb_stop_foto = ReplyKeyboardMarkup([[bt_stop_foto]], resize_keyboard=True)

bt_get_event_list = InlineKeyboardButton(text='Посмотреть записи', callback_data='get_event_list')

bt_add_sert = InlineKeyboardButton(text="Добавить сертификат", callback_data='add_sert')
kb_get_event_list = InlineKeyboardMarkup(row_width=1)
kb_get_event_list.row(bt_get_event_list)
kb_get_event_list.row(bt_add_sert)



list_raboti = []

for dir in os.listdir('raboti'):
    list_raboti.append([InlineKeyboardButton(text=dir, callback_data=dir)])
kb_raboti = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_raboti)


bt_back_raboti = InlineKeyboardButton(text='Назад к работам', callback_data='raboti')
kb_back_raboti = InlineKeyboardMarkup(row_width=1).row(bt_back_raboti)
