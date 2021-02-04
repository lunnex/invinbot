from aiogram import types
from misc import dp
from dbWorks import getMessage
#from dbWorks import addActive
from dbWorks import parseInfo
import datetime
import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class AddActiveStates(StatesGroup):
    waitingForLink = State()
    waitingForAmount = State()
    waitingForPrice = State()

#Сообщения о состоянии активов каждые 4 часа
@dp.message_handler(commands=['start'])
async def getInfoCommand (message: types.Message):
    msg = ''
    msg = getMessage.putInfoIntoMsg()

    await message.answer('`'+msg+'`',parse_mode = 'Markdown')
    await asyncio.sleep(14400)

    now = datetime.datetime.now()
    if (now.hour >= 8):
        parseInfo.threadWorks(parseInfo.getQuantyOfLinks(parseInfo.getAbsPathOfLinks()))
        await getInfoCommand(message)

#Немедленное сообщение о состоянии активов
@dp.message_handler(commands=['info'])
async def getInstantInfoCommand (message: types.Message):
    parseInfo.threadWorks(parseInfo.getQuantyOfLinks(parseInfo.getAbsPathOfLinks()))
    msg = ''
    msg = getMessage.putInfoIntoMsg()
    await message.answer('`'+msg+'`',parse_mode = 'Markdown')

#Добавляем новый актив
@dp.message_handler(commands=['addactive'], state = "*")
async def addActiveCommand (message: types.Message):
    await message.answer('`'+'Добавляю данные о новом активе'+'`',parse_mode = 'Markdown')
    await message.answer('`'+'Пожалуста, введите ссылку на актив'+'`',parse_mode = 'Markdown')
    await AddActiveStates.waitingForLink.set()

@dp.message_handler(state=AddActiveStates.waitingForLink, content_types=types.ContentTypes.TEXT)
async def addLinkActiveCommand(message: types.Message, state: FSMContext):
    link = message.text
    with open(parseInfo.getAbsPathOfLinks(), "a", encoding = 'utf8') as file:
        file.write(link + '\n')
        file.close()
    await message.answer('`'+'Пожалуста, введите количество ценных бумаг'+'`',parse_mode = 'Markdown')
    await AddActiveStates.waitingForAmount.set()
    #a_ID = parseInfo.getQuantyOfLinks(parseInfo.getAbsPathOfLinks()) + 1
