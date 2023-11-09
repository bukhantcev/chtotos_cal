import os

from db_config import add_new_procedura, cursor, connect, PATH, create_table, update_procedura
from uslugi import proceduri


def fill_db():
    for i in range(len(proceduri.proc_1)):
        name = proceduri.proc_1[i][0]
        time_minute = proceduri.proc_1[i][1]
        price = proceduri.proc_1[i][2]
        command = 'ukol'
        description = proceduri.proc_1[i][3]
        new_proc = (name, time_minute, price, command, description)

        add_new_procedura(new_proc)
        new_data = (f"{command}_{str(cursor.lastrowid)}", cursor.lastrowid)

        update_procedura(new_data)
    print('db zapolnena')



