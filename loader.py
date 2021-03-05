from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = "1639196649:AAF_Y79dJvaeU0HjwTPLvtPH6wKUzTrOYJA"

bot = Bot(token=token, parse_mode=types.ParseMode.MARKDOWN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


