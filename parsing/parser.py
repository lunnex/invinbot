import requests
from bs4 import BeautifulSoup
import lxml
from threading import Timer
from time import sleep, time
import time
import os

url = ['https://bcs-express.ru/kotirovki-i-grafiki/moex', 'https://bcs-express.ru/kotirovki-i-grafiki/sber', 'https://bcs-express.ru/kotirovki-i-grafiki/mtss', 'https://bcs-express.ru/kotirovki-i-grafiki/rtkmp']
moexUrl = ['https://place.moex.com/products/etfs/FXIT', 'https://place.moex.com/products/bonds/SU25083RMFS5']
invfUrl = ['https://investfunds.ru/bonds/409765/', 'https://investfunds.ru/bonds/410621/', 'https://investfunds.ru/stocks/Mail-ru-Group-dr/']
prices = []
lines = []
amounts = [30.0, 10.0, 10.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0]
total = 0
lastTotal = 0

def req(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text

def GetNameOfActiveBCS(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_ = "quote-head__name")
    if len(name.string) < 9:
        return name.string + '\t\t'
    else:
        return name.string + '\t'

def GetPriceOfActiveBCS(html):
    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('div', class_ = "quote-head__price-value js-quote-head-price js-price-close")
    pricestr = price.string
    pricestr = pricestr.replace(',', '.')
    pricestr = pricestr.replace('', '')
    return pricestr

def GetNameOfActiveMoex(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('span', class_ = "span stock-company__heading-part")
        namestr = name.string
    except:
        name = soup.find('span', style = "margin-top:0;margin-left:5px;")
        namestr = name.string
    namestr = ''.join(namestr.split())
    if len(namestr) < 5:
        return namestr + '\t\t'
    else:
        return namestr + '\t'

def GetPriceOfActiveMoex(html):
    soup = BeautifulSoup(html, 'lxml')
    priceInt = soup.find('span', class_ = "int")
    priceFrac = soup.find('span', class_ = "alt")
    priceInt = priceInt.string
    priceFrac = priceFrac.string
    priceInt = priceInt.replace(',', '')
    priceFrac = priceFrac.replace (' ₽', '')
    pricestr = priceInt + priceFrac
    pricestr = pricestr.replace (',', '.')
    return pricestr

def GetNameOfActiveInv(html):
    soup = BeautifulSoup(html, 'lxml')
    namestr = soup.findAll('div', class_ = "value")
    namestrs = []
    for i in namestr:
        namestrs.append(i.string)
    namestr = namestrs[5].string
    a = soup.find('span', class_ = "item")
    a = a.string
    if a == 'Mail.ru Group, депозитарная расписка (US5603172082, MAIL, RL9A)':
        namestr = soup.find('span', class_ = "item")
        namestr = namestr.string
    if len(namestr) < 5:
        return namestr + '\t\t'
    else:
        return namestr + '\t'

def GetPriceOfActiveInv(html):
    soup = BeautifulSoup(html, 'lxml')
    priceInt = soup.findAll('div', class_ = "price left")
    priceInts = []
    for i in priceInt:
        priceInts.append(i.string)
    try:
        priceInt = priceInts[1].string
        #print(priceInts)
    except:
        priceInt = priceInts[0].string
        #print(priceInts)
    priceInt = priceInt.replace(',', '.')
    priceInt = priceInt.replace(' ', '')
    return priceInt
    #return '1' + '\t'

def GetBCS():
    with open(r'rrrrr.txt', 'a', encoding='utf-8') as file:
        for i in range (0, len(url)):
            file.write('Акции ')
            file.write(str(GetNameOfActiveBCS(req(url[i]))))
            file.write(str(GetPriceOfActiveBCS(req(url[i]))))
            prices.append(float(GetPriceOfActiveBCS(req(url[i]))))
            file.write(' * '+ str(amounts[i]) + '\t')
            sum = round(amounts[i]*prices[i],2)
            file.write(' = '+ str(sum))
            file.write(' last.' + lines[i])
            #delta = (float((amounts[i] * prices[i]) / float(lines[i]) - 1.0 ))*100
            a = float(lines[i])
            b = float(amounts[i] * prices[i])
            delta = (b/a - 1.0)*100
            percents = round(delta,2)
            file.write(str(percents)+ '% \n')
        file.close()

def GetMoex():
    with open(r'rrrrr.txt', 'a', encoding='utf-8') as file:
        for i in range (0, len(moexUrl)):
            if moexUrl[i].find('etfs') != -1:
                file.write('Фонд  ')
            else:
                file.write('Облиг ')
            file.write(str(GetNameOfActiveMoex(req(moexUrl[i]))))
            file.write(str(GetPriceOfActiveMoex(req(moexUrl[i]))))
            prices.append(float(GetPriceOfActiveMoex(req(moexUrl[i]))))
            file.write(' * '+ str(amounts[i + len(url)]) + '\t')
            sum = round(amounts[i + len(url)]*prices[i + len(url)],2)
            file.write(' = '+ str(sum))
            file.write(' last.' + lines[i + len(url)])
            #delta = (float((amounts[i + len(url)]*prices[i + len(url)]) / float(lines[i + len(url)]) - 1.0))*100
            a = float(lines[i + len(url)])
            b = float(amounts[i + len(url)]*prices[i + len(url)])
            #delta = (1.0 - float(lines[i + len(url)]) / float(amounts[i + len(url)]*prices[i + len(url)]))*100
            delta = (1.0 - a/b)*100
            percents = round(delta,2)
            file.write(str(percents)+ '% \n')
        file.close()

def GetInv():
    with open(r'rrrrr.txt', 'a', encoding='utf-8') as file:
        for i in range (0, len(invfUrl)):
            if invfUrl[i].find('bonds') != -1:
                file.write('Облиг  ')
            else:
                file.write('Акции ')
            file.write(str(GetNameOfActiveInv(req(invfUrl[i]))))
            file.write(str(GetPriceOfActiveInv(req(invfUrl[i]))))
            prices.append(float(GetPriceOfActiveInv(req(invfUrl[i]))))
            file.write(' * '+ str(amounts[i + len(url) + len(moexUrl)]) + '\t')
            sum = round(amounts[i + len(url) + len(moexUrl)]*prices[i + len(url) + len(moexUrl)],2)
            file.write(' = '+ str(sum))
            file.write(' last.' + lines[i + len(url) + len(moexUrl)])
            #delta = (float(((amounts[i + len(url) + len(moexUrl)]) * prices[i + len(url) + len(moexUrl)]) / float(lines[i + len(url) + len(moexUrl)]) - 1.0))*100
            #delta = (1.0 - float(lines[i + len(url) + len(moexUrl)]) / float((amounts[i + len(url) + len(moexUrl)]) * prices[i + len(url) + len(moexUrl)]))*100
            b = float((amounts[i + len(url) + len(moexUrl)]) * prices[i + len(url) + len(moexUrl)])
            a = float(lines[i + len(url) + len(moexUrl)])
            delta = (1.0 - a/b)*100
            percents = round(delta,2)
            file.write(str(percents)+ '% \n')
        file.close()

def GetInfo():

    total = 0
    lastTotal = 0
    with open(r'rrrrr.txt', 'w', encoding='utf-8') as file:
        file.write('Милорд')
        file.close()

    with open(r'rrrrrt.txt', 'r', encoding='utf-8') as filet:
        for line in filet:
            lines.append(line)
        filet.close()

    prices.clear()

    GetBCS()
    GetMoex()
    GetInv()

    with open(r'rrrrr.txt', 'a', encoding='utf-8') as file:
        for i in range (0, len(url) + len(moexUrl) + len(invfUrl)):
            total += amounts[i]*prices[i]
            lastTotal += float(lines[i])
            total = round(total,2)
            lastTotal = round(lastTotal,2)
            percents = (1 - lastTotal/total)*100
        file.write('Итог: '+ str(total) + ' (' + str(lastTotal) + ') ' + ' ' + str(round(percents,2)) + '%')
        file.close()

    with open(r'rrrrr.txt', 'r', encoding='utf-8') as file:
        lns = file.read()
        file.close()

    with open(r'rrrrr.txt', 'w', encoding='utf-8') as file:
        if (total > lastTotal):
            lns = lns.replace('Милорд', 'Казна пополняется, Милорд!\n')
        else:
            lns = lns.replace('Милорд', 'Казна пустеет, Милорд!\n')
        file.write(lns)
        #file.write("\n")
        file.close()

    with open(r'rrrrrt.txt', 'w', encoding='utf-8') as fileOfPrices:
        for i in range (0, len(url)+len(moexUrl)+len(invfUrl)):
            fileOfPrices.write(str(amounts[i]*prices[i]) + '\n')
        fileOfPrices.close()
        lines.clear()

def getR():
    return(os.path.abspath(r'rrrrr.txt'))

def getRt():
    return(os.path.abspath(r'rrrrrt.txt'))


#GetInfo()
