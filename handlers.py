from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command, Text

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db import *

from loader import dp, bot


def root_categories():
	markup = InlineKeyboardMarkup(row_width=3)
	for item in Category.all():
		markup.insert(InlineKeyboardButton(text=f"{item.undercategory}",callback_data=f"item"))
	return markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
	await message.answer("----",reply_markup=root_categories())





