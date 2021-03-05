from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = "1408510148:AAG8ONDaaz3sfzbNE5_sGKNw0sgaWf7jAaI"

bot = Bot(token=token, parse_mode=types.ParseMode.MARKDOWN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


