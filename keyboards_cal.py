import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


year = 0

list_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
list_text = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
current_year = datetime.date.today().year
curent_month = datetime.date.today().month
new_list = list_month[curent_month-1:]+list_month[:curent_month-1]
current_index = 0
next_index = 0
final_list_bt = []
for i in new_list:
    current_index = list_month.index(i)
    next_index = new_list.index(i)
    if next_index-current_index>0:
        year = current_year + 1
        final_list_bt.append([InlineKeyboardButton(text=f'{list_text[current_index]} {year}',
                                                   callback_data=f'{year}-{list_month[current_index]}')])
    else:
        year = current_year
        final_list_bt.append([InlineKeyboardButton(text=f'{list_text[current_index]} {year}',
                                                   callback_data=f'{year}-{list_month[current_index]}')])

cal_kb = InlineKeyboardMarkup(inline_keyboard=final_list_bt)

'''__________________________________________________________________________________________________________________'''


import datetime


def create_day_table(month: int):
    days_in_month = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    curent_month = month
    days_bt_text = []
    num = 1
    for i in range(5):
        if num >= int(days_in_month[curent_month]):
            break
        row_list = []
        for k in range(7):
            if num > int(days_in_month[curent_month]):
                break
            row_list.append(InlineKeyboardButton(text=num, callback_data=num))
            num = num+1

        days_bt_text.append(row_list)
    return days_bt_text

'''______________________________________________________________________________________________________________________'''


bt_yes = InlineKeyboardButton(text= 'Записать', callback_data='event_yes')
bt_no = InlineKeyboardButton(text= 'Отменить', callback_data='event_no')

kb_creat_event = InlineKeyboardMarkup(row_width=2)
kb_creat_event.row(bt_yes, bt_no)









