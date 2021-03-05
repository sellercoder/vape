from aiogram.dispatcher.filters.state import StatesGroup, State

class AddGood(StatesGroup):
	name = State()
    price = State()
    image = State()
    category = State()

