import sqlite3
import os

def strNormalize(s):
    s = s.replace('"', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(',', '')
    s = s.replace("'", '')
    return s

connection = sqlite3.connect(os.path.abspath('inv.db'))
print (os.path.abspath('inv.db'))
cursor = connection.cursor()

cursor.execute('select* from infonow')
rows = cursor.fetchall()

# получаем путь к текстовому файлу с тектом для отправки ползователю
def getAbsPathOfMSGFile():
    return(os.path.abspath(r'msg.txt'))

def putInfoIntoMsg():
    i=0
    totalsum = 0.0
    totalMP = 0.0 #утреняя цена
    totalChange = 0.0
    insstr = ''
    a = getAbsPathOfMSGFile() #путь к текстовому файлу с тектом для отправки ползователю
    with open(a, 'w', encoding='utf-8') as file:
        file.write ('%-8s'%'Название'+'|'+'%-6s'%'Цена'+'|'+'%+.*s'%(7,'Изменение')+'|'+'%-8s'%'Сумма'+ '|'+'\n')
        file.write ('--------+------+-------+--------|\n')
        for row in rows:
            i = i+1
            cursor.execute(f'select a_name from infonow where a_ID = {i}')
            name = cursor.fetchone()
            strname = str(name)
            strname = strNormalize(strname)
            strname = strname + "            "
            insstr = '%+.*s'%(8, strname) + '|'
            #insstr = insstr.replace(' ', '  ')
            file.write (insstr)

            cursor.execute(f'select a_price from infonow where a_ID = {i}')
            price = cursor.fetchone()
            strprice = str(price)
            strprice = strNormalize(strprice)
            strprice = strprice + "            "
            insstr = '%+.*s'%(6, strprice)+ '|'
            #insstr = insstr.replace(' ', '  ')
            file.write (insstr)

            cursor.execute(f'select change from infonow where a_ID = {i}')
            change = cursor.fetchone()
            strchange = str(change)
            strchange = strNormalize(strchange)
            strchange = strchange + "            "
            insstr = '%+.*s'%(5, strchange)+' %'+ '|'
            #insstr = insstr.replace(' ', '  ')
            file.write (insstr)

            cursor.execute(f'select a_sum from infonow where a_ID = {i}')
            sum = cursor.fetchone()
            cursor.execute(f'select morningPrice*amount from infonow where a_ID = {i}')
            morningPrice = cursor.fetchone()
            strMP = str(morningPrice)
            strMP = strNormalize(strMP)
            doubMP = float(strMP)
            cursor.execute(f'select type from infonow where a_ID = {i}')
            type = cursor.fetchone()
            strtype = str(type)
            strtype = strNormalize(strtype)
            strsum = str(sum)
            strsum = strNormalize(strsum)
            if (strtype == 'Облигации'):
                doubsum = float(strsum)*10
                doubMP = doubMP*10
            else:
                doubsum = float(strsum)*1
                doubMP = doubMP*1
            strsum = str(doubsum)
            strsum = strsum + "            "
            insstr = '%+.*s'%(8, strsum)+ '|'+ '\n'
            #insstr = insstr.replace(' ', '  ')
            file.write (insstr)
            file.write ('--------+------+-------+--------|\n')
            totalsum = doubsum + totalsum
            totalMP = doubMP + totalMP
        totalChange = (totalsum/totalMP - 1)*100
        file.write ('Итог: '+ str(totalsum) +' ('+str(round(totalMP, 2)) +') '+ str(round(totalChange,3))+ '%')
    file.close()
