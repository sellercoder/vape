from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from states import AddGood
from db import *
from loader import dp, bot

def get_categories():
	lst = []
	for category in Category.all():
		lst.append(category.category)
		lst.append(category.undercategory)
	mylist = list(dict.fromkeys(lst))
	return mylist

def categories_menu():
	markup = InlineKeyboardMarkup(row_width=3)
	markup.row(InlineKeyboardButton(text=f"Добавить товар",callback_data="add"))
	# for category in get_categories():
	# 	markup.insert(InlineKeyboardButton(text=f"{category}", callback_data=f"category:{category}"))
	return markup

def set_category():
	markup = ReplyKeyboardMarkup(row_width=3)
	for category in get_categories():
		markup.insert(KeyboardButton(text=f"{category}"))
	return markup

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
	await message.answer(text=f"🤖 Привет! я минибот, служу для того, чтобы добавлять товары в магазин `VapeLove_bot`", reply_markup=categories_menu())

@dp.callback_query_handler(text_contains="add", state="*")
async def admin_edit(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text(text=f"Название товара")
	await AddGood.name.set()

@dp.message_handler(state=AddGood.name)
async def enter_name(message: types.Message, state: FSMContext):
	name = message.text
	good = Good()
	good.name = name
	await message.answer(f"Теперь пришли цену")
	await AddGood.price.set()
	await state.update_data(good=good)

@dp.message_handler(regexp=r"^(\d+)$", state=AddGood.price)
async def enter_price(message: types.Message, state: FSMContext):
	data = await state.get_data()
	good: Good = data.get("good")
	price = message.text
	good.price = price
	await AddGood.image.set()
	await state.update_data(good=good)
	await message.answer(f"`Теперь пришли фото товара`")

@dp.message_handler(state=AddGood.price)
async def not_price(message: types.Message, state: FSMContext):
    await message.answer(f"Нужно число...")

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AddGood.image)
async def sned_tt(message: Message, state: FSMContext):
	data = await state.get_data()
	good: Good = data.get("good")
	good.image = message.photo[-1].file_id
	await AddGood.category.set()
	await state.update_data(good=good)
	await message.answer_photo(good.image,caption=f"{good.name}\n{good.price}")
	await message.answer("Категория", reply_markup=set_category())

@dp.message_handler(state=AddGood.category)
async def sned_ttd(message: Message, state: FSMContext):
	data = await state.get_data()
	good: Good = data.get("good")
	good.category = message.text
	good.save()
	await message.answer_photo(good.image,caption=f"{good.name}\n{good.price}\n{good.category}")
	await message.answer("товар добавлен", reply_markup=ReplyKeyboardRemove())
	await state.reset_state()







