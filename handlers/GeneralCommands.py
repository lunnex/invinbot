from aiogram import types
from misc import dp
#from parsing import parser
from dbWorks import getMessage
from threading import Timer
from time import sleep, time
import datetime
import time

#@dp.message_handler(commands=['start'])
#async def StartCommand (message: types.Message):
#    await message.answer("Начинаю отслеживать состояние счёта")

@dp.message_handler(commands=['start'])
async def GetInfoCommand (message: types.Message):
    #timer = Timer(interval=60,function = parser.GetInfo())
    while True:
        now = datetime.datetime.now()
        if now.hour >= 0:
            getMessage.putInfoIntoMsg()
            a = getMessage.getAbsPathOfMSGFile()
            with open(a, 'r', encoding='utf-8') as file:
                lines = file.read()
            file.close()
            #parser.GetInfo()
            await message.answer('`'+lines+'`',parse_mode = 'Markdown')
            time.sleep(14400)
            await GetInfoCommand(message)
