import sqlite3
import os
import parseInfo as parseInfo

def DBInsert(a_ID, a_name, amount, type):
    connection = sqlite3.connect(parseInfo.getAbsPathOfDB())
    cursor = connection.cursor()

    try:
        cursor.execute(f'select* from infonow where a_name = (?)', (name))
    except:
        cursor.execute(f'insert into actives a_ID = (?), a_name = (?), amount = (?), type = (?)', (ID, name, amount, type))
        cursor.execute(f'insert into infonow a_ID = (?), a_name = (?), amount = (?), type = (?)', (ID, name, amount, type))
        connection.commit()
