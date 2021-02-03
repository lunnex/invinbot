from aiogram import types
from misc import dp
from dbWorks import getMessage
from dbWorks import parseInfo
import datetime
import time
from aiogram.utils import executor
import asyncio

#Сообщения о состоянии активов каждые 4 часа
@dp.message_handler(commands=['start'])
async def getInfoCommand (message: types.Message):
    now = datetime.datetime.now()
    if (now.hour >=0):#тестовое значение, потом поменять!
        getMessage.putInfoIntoMsg()
        a = getMessage.getAbsPathOfMSGFile()
        with open(a, 'r', encoding='utf-8') as file:
            lines = file.read()
        file.close()
        await message.answer('`'+lines+'`',parse_mode = 'Markdown')
    await asyncio.sleep(10) #тестовое значение, потом поменять!
    await getInfoCommand(message)


#Немедленное сообщение о состоянии активов
@dp.message_handler(commands=['info'])
async def getInstantInfoCommand (message: types.Message):
    parseInfo.threadWorks(parseInfo.getQuantyOfLinks(parseInfo.getAbsPathOfLinks()))
    getMessage.putInfoIntoMsg()
    a = getMessage.getAbsPathOfMSGFile()
    with open(a, 'r', encoding='utf-8') as file:
        lines = file.read()
    file.close()
    await message.answer('`'+lines+'`',parse_mode = 'Markdown')
