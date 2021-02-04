import sqlite3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import lxml
import threading
import os

ua = UserAgent()
usrData = {'User-Agent': ua.random}

#Получаем путь файла с ссылками на активы
def getAbsPathOfLinks():
    return (os.path.abspath('links'))

#Получаем путь к базе данных
def getAbsPathOfDB():
    return (os.path.abspath('inv.db'))

#Получаем страничку
def req(url):
    page = requests.get(url, headers = usrData)
    return (page.text)

#Получаем название актива
def getName(page):
    soup = BeautifulSoup(page, 'lxml')
    name = soup.find('h1', class_ = "quote-head__name")
    #namestr = str(name.text)
    return (name.text)

#Получаем цену актива
def getPrice(page):
    soup = BeautifulSoup(page, 'lxml')
    price = (soup.find(class_ = "quote-head__price-value js-quote-head-price js-price-close"))
    return price.text

#Получаем изменение цены актива с начала дня
def getChange(page):
    soup = BeautifulSoup(page, 'lxml')
    change = (soup.find(class_ = "quote-head__price-change js-profit-percent"))
    return change.text

#Получаем количество ссылок
def getQuantyOfLinks(linkPath):
    i = 0
    with open(linkPath) as file:
        for lines in file.readlines():
            i = i + 1
    return i

#Убираем лишние символы из полученных названий
def stringNormalizeN(string):
    string = string.replace(u'\xa0',u'')
    return string

#Убираем лишние символы из полученных цен
def stringNormalizeP(string):
    string = string.replace("%","")
    string = string.replace(",",".")
    string = string.replace(u'\xa0',u'')
    return string

#Работа с БД
def transaction(strurl, quantyOfLinks, linkPath):
    text = req(strurl)
    name = stringNormalizeN(str(getName(text)))
    price = float(stringNormalizeP(str(getPrice(text))))
    change = float(stringNormalizeP(str(getChange(text))))

    connection = sqlite3.connect(getAbsPathOfDB())
    cursor = connection.cursor()

    try:
        cursor.execute(f'update infonow set a_price = (?) where a_name = (?)', (price, name))
        cursor.execute(f'update infonow set change = (?) where a_name = (?)', (change, name))
        connection.commit()
    except:
        print('error')

#Создаём потоки и выполняем их
def threadWorks(quantyOfLinks):
    url = []
    threads = []
    linkPath = getAbsPathOfLinks()
    quantyOfLinks = getQuantyOfLinks(linkPath)

    with open(linkPath, "r", encoding = 'utf8') as file:
        url = file.readlines()

    for i in range(0, quantyOfLinks):
        strurl = url[i]
        strurl = strurl.rstrip()
        threads.append(threading.Thread(target = transaction, args = (strurl, quantyOfLinks, linkPath)))

    for i in range(0, quantyOfLinks):
        threads[i].start()
    for i in range(0, quantyOfLinks):
        threads[i].join()
