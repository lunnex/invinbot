from aiogram import executor
from misc import dp
from handlers import GeneralCommands
from aiogram.utils import executor
import asyncio

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
