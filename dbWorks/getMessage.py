import sqlite3
import os

def strNormalize(s):
    s = s.replace('"', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(',', '')
    s = s.replace("'", '')
    s = s.replace("[", '')
    s = s.replace("]", '')
    return s

def prRound(s):
    s = str(round(float(s),2))
    return s

def countRows(cursor):
    cursor.execute('select count(a_name) from infonow')
    rows = int(strNormalize(str(cursor.fetchall())))
    return rows

def putInfoIntoMsg():
    message = ''
    i=0
    totalsum = 0.0
    totalMP = 0.0 #утреняя цена
    totalChange = 0.0
    insstr = ''

    connection = sqlite3.connect(os.path.abspath('inv.db'))
    cursor = connection.cursor()

    message = message + ('%-8s'%'Название'+'|'+'%-6s'%'Цена'+'|'+'%+.*s'%(7,'Изменение')+'|'+'%-8s'%'Сумма'+'\n')
    message = message + ('--------+------+-------+---------\n')
    for i in range(0, countRows(cursor)):
        i = i+1
        cursor.execute(f'select a_name from infonow where a_ID = {i}')
        name = cursor.fetchone()
        strname = str(name)
        strname = strNormalize(strname)
        strname = strname + "            "
        insstr = '%+.*s'%(8, strname) + '|'
        message = message + insstr

        cursor.execute(f'select a_price from infonow where a_ID = {i}')
        price = cursor.fetchone()
        realPrice = prRound(float(strNormalize(str(price))))
        strprice = str(realPrice)
        strprice = strNormalize(strprice)
        strprice = strprice + "            "
        insstr = '%+.*s'%(7, strprice)+ '|'
        message = message + insstr

        cursor.execute(f'select change from infonow where a_ID = {i}')
        change = cursor.fetchone()
        strchange = str(change)
        strchange = strNormalize(strchange)
        strchange = strchange + "            "
        insstr = '%+.*s'%(4, strchange)+' %'+ '|'
        message = message + insstr

        cursor.execute(f'select a_price*amount from infonow where a_ID = {i}')
        sumOfActive = cursor.fetchone()
        realSumOfActive = prRound(float(strNormalize(str(sumOfActive))))
        strSumOfActive = strNormalize(realSumOfActive)
        strSumOfActive = strSumOfActive + "            "
        insstr = '%+.*s'%(8, strSumOfActive)
        message = message + insstr

        message = message + '\n'

    message = message + ('---------------------------------\n')
    cursor.execute('select sum(a_price*amount) from infonow')
    sum = strNormalize(str(cursor.fetchone()))
    cursor.execute('select sum(morningPrice*amount) from infonow')
    morSum = strNormalize(str(cursor.fetchone()))
    totalChange = ((float(str(sum))/float(str(morSum))) - 1)*100

    message = message + ('Итог: '+ prRound(sum) +' ('+ prRound(morSum) +') '+ prRound(totalChange)+ '%')
    connection.close()
    return message
