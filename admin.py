from aiogram.types import Message
from db_config import add_new_procedura, find_procedura, delete_procedura, cursor, add_description, update_procedura
from list_commands import list_commands
from loader import dp


# ДОБАВЛЕНИЕ ПРОЦЕДУРЫ. ПРИМЕР СООБЩЕНИЯ - /new_procedura, Имя, Продолжительность, Цена, Команда
@dp.message_handler(commands=['new_procedura,'])
async def add_procedura(message: Message, admin:bool):
    if admin:
        name, time_minute, price, command = message.text.split(', ')[1:]
        print(name, time_minute, price, command)
        procedura = (name, time_minute, price, command)
        add_new_procedura(procedura)
        new_data = (f"{message.text.split(', ')[4]}_{str(cursor.lastrowid)}", cursor.lastrowid)
        print(new_data)
        update_procedura(new_data)

        await message.answer('Процедура добавлена!')
    else:
        await message.answer('У вас нет прав администратора!')



# ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ПРОЦЕДУРЕ ПО ИМЕНИ. ПРИМЕР СООБЩЕНИЯ - /find_procedura Имя
@dp.message_handler(commands=['find_procedura'])
async  def find_procedura_command(message: Message,admin:bool):
    if admin:
        name = (message.text.split()[1],)
        result = find_procedura(name)
        if not result:
            result = 'Такой процедуры нет'
        await message.answer(text=result)
    else:
        await message.answer('У вас нет прав администратора!')

# УДАЛЕНИЕ ПРОЦЕДУРЫ ПО id, ПРИМЕР СООБЩЕНИЯ - /delete_procedura id
@dp.message_handler(commands=['delete_procedura'])
async def delete_procedura_command(message: Message, admin:bool):
    if admin:
        try:
            procedura_id = message.text.split()[1]
            if procedura_id.isdigit():
                delete_procedura((int(procedura_id),))
                await message.answer('Процедура удалена.')
            else:
                await message.answer('Нужно прислать id процедуры')
        except:
            await message.answer('Процедуры с таким id не существует!')
    else:
        await message.answer('У вас нет прав администратора!')


# ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ВСЕХ ПРОЦЕДУРАХ. ПРИМЕР СООБЩЕНИЯ - /find_allprocedura
@dp.message_handler(commands=['find_allproceduri'])
async  def find_allproceduri_command(message: Message, admin:bool):
    if admin:
        cursor.execute('SELECT * FROM proceduri')
        await message.answer(cursor.fetchall())
    else:
        await message.answer('У вас нет прав администратора!')
#ПОЛУЧЕНИЕ СПИСКА КОМАНД
@dp.message_handler(commands=['help'])
async  def help(message: Message, admin:bool):
    if admin:
        await message.answer(list_commands)
    else:
        await message.answer('У вас нет прав администратора!')

#Добавление описания
@dp.message_handler(commands=['add_description'])
async def add_description_cmd(message: Message, admin:bool):
    if admin:
        descr = message.text.split(' $ ')[1]
        id = message.text.split(' $ ')[2]
        new_description = (descr, id)
        add_description(new_description)
        print(f'Описание добавлено в процедуру № {id}')
        await message.answer(f'Описание добавлено в процедуру № {id}')
    else:
        await message.answer('У вас нет прав администратора!')