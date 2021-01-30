from aiogram import types
from misc import dp
from parsing import parser
from threading import Timer
from time import sleep, time
import time

@dp.message_handler(commands=['start'])
async def StartCommand (message: types.Message):
    await message.answer("Начинаю отслеживать состояние счёта")

@dp.message_handler(commands=['getinfo'])
async def GetInfoCommand (message: types.Message):
    #timer = Timer(interval=60,function = parser.GetInfo())
    #while True:
        a = parser.getR()
        with open(a, 'r', encoding='utf-8') as file:
            lines = file.read()
        file.close()
        parser.GetInfo()
        await message.answer(lines)
        time.sleep(160)
        await GetInfoCommand(message)
