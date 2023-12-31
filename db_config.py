import sqlite3

PATH = 'db/db_proceduri.db'
connect = sqlite3.connect(PATH)
cursor = connect.cursor()


# PROCEDURI

# СОЗДАНИЕ ТАБЛИЦЫ ПРОЦЕДУРЫ
def create_table():
    cursor.execute('DROP TABLE IF EXISTS proceduri')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proceduri (proceduri_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR,
     time_minute VARCHAR, price VARCHAR, command VARCHAR, description VARCHAR, foto BLOB)''')
    connect.commit()


# СОЗДАНИЕ ТАБЛИЦЫ КЛИЕНТЫ
def create_table_klients():
    cursor.execute('''CREATE TABLE IF NOT EXISTS klients (tg_id INTEGER 
    PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, tg_username VARCHAR, last_procedure VARCHAR, 
    date_recording VARCHAR, date_vizit VARCHAR, 
    status_news VARCHAR, phone VARCHAR, procedure VARCHAR, status_recording VARCHAR)''')
    connect.commit()


# СОЗДАНИЕ ТАБЛИЦЫ ФОТО СЕРТИФИКАТЫ
def create_table_photo_sertificate():
    cursor.execute('''CREATE TABLE IF NOT EXISTS photo_sertificate (id INTEGER 
    PRIMARY KEY AUTOINCREMENT, name VARCHAR, photo_id VARCHAR, activ_index INTEGER)''')
    connect.commit()


# ДОБАВИТЬ РЯДЫ
def add_new_procedura(new_procedura: tuple):
    cursor.execute('''INSERT INTO proceduri (name, time_minute, price, command, description) VALUES (?, ?, ?, ?, ?)''',
                   new_procedura)
    connect.commit()


def add_new_sert(new_sert: tuple):
    cursor.execute(
        '''INSERT INTO photo_sertificate (name, photo_id) VALUES (?, ?)''',
        new_sert)
    connect.commit()


def add_new_klient(new_klient: tuple):
    cursor.execute(
        '''INSERT INTO klients (tg_id, first_name, last_name, tg_username) VALUES (?, ?, ?, ?)
         ON CONFLICT (tg_id) DO UPDATE
                    SET 
                    first_name = first_name, last_name = last_name''', new_klient)
    connect.commit()


# ИЗМЕНЕНИЕ КОМАНДЫ ПО id
def update_procedura(new_data: tuple):
    cursor.execute('''UPDATE proceduri SET command=? WHERE proceduri_id=?''', new_data)
    connect.commit()


# ПОЛУЧИТЬ ПРОЦЕДУРУ ПО ИМЕНИ
def find_procedura(proceduri_id: tuple):
    procedura = cursor.execute('''SELECT * FROM proceduri WHERE proceduri_id=?''', proceduri_id).fetchall()
    return procedura


def find_name_procedure(name: tuple):
    procedura = cursor.execute('''SELECT last_procedure FROM klients WHERE tg_id=?''', name).fetchall()
    return procedura


# ПОЛУЧИТЬ id ПРОЦЕДУРЫ ПО КОМАНДЕ
def find_idproceduri(command: tuple):
    id_proc = cursor.execute('''SELECT proceduri_id  FROM proceduri WHERE command=?''', command).fetchall()
    return id_proc


# УДАЛЕНИЕ ПРОЦЕДУРЫ ПО id

def delete_procedura(proceduri_id: tuple):
    cursor.execute('''DELETE FROM proceduri WHERE proceduri_id=?''', proceduri_id)
    connect.commit()


# ИЗМЕНЕНИЕ КОЛОНКИ ПО tg_id
def update_klient(new_data: tuple, column_name):
    cursor.execute(f'UPDATE klients SET {column_name}=? WHERE tg_id=?', new_data)
    connect.commit()


def update_photo_sertificate(new_data: tuple, column_name):
    cursor.execute(f'UPDATE photo_sertificate SET {column_name}=? WHERE photo_id=?', new_data)
    connect.commit()


# ДОБАВИТЬ ОПИСАНИЕ ПРОЦЕДУРЫ /add_description Описание$ id
def add_description(new_description: tuple):
    cursor.execute('''UPDATE proceduri SET uslugi=? WHERE proceduri_id=?''', new_description)
    connect.commit()


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def add_photo(new_foto: tuple):
    cursor.execute('''UPDATE proceduri SET foto=? WHERE proceduri_id=?''', new_foto)
    connect.commit()
