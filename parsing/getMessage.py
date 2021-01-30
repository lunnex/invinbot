import sqlite3

def strNormalize(s):
    s = s.replace('"', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(',', '')
    s = s.replace("'", '')
    return s

connection = sqlite3.connect(r"C:\Users\ilyak\eclipse-workspace\Parser\src\inv.db")
cursor = connection.cursor()

cursor.execute('select* from infonow')
rows = cursor.fetchall()

i=0
totalsum = 0.0
totalMP = 0.0
totalChange = 0.0
with open(r'msg.txt', 'w', encoding='utf-8') as file:
    file.write ('%-8s'%'Название'+'|'+'%-7s'%'Цена'+'|'+'%-4s'%'Изменение'+'|'+'%-8s'%'Сумма'+ '|'+'\n')
    file.write ('-----------------------------------|\n')
    for row in rows:
        i = i+1
        cursor.execute(f'select a_name from infonow where a_ID = {i}')
        name = cursor.fetchone()
        strname = str(name)
        strname = strNormalize(strname)
        strname = strname + "            "
        file.write ('%+.*s'%(8, strname) + '|')

        cursor.execute(f'select a_price from infonow where a_ID = {i}')
        price = cursor.fetchone()
        strprice = str(price)
        strprice = strNormalize(strprice)
        strprice = strprice + "            "
        file.write ('%+.*s'%(7, strprice)+ '|')

        cursor.execute(f'select change from infonow where a_ID = {i}')
        change = cursor.fetchone()
        strchange = str(change)
        strchange = strNormalize(strchange)
        strchange = strchange + "            "
        file.write ('%+.*s'%(7, strchange)+' %'+ '|')

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
        file.write ('%+.*s'%(8, strsum)+ '|'+ '\n')
        file.write ('-----------------------------------|\n')
        totalsum = doubsum + totalsum
        totalMP = doubMP + totalMP
    totalChange = (totalsum/totalMP - 1)*100
    file.write ('Итог: '+ str(totalsum) +' ('+str(round(totalMP, 2)) +') '+ str(round(totalChange,4))+ ' %')

def getAbsPathOfMSGFile():
    return(os.path.abspath(r'msg.txt'))
