from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import aiosqlite
import aiohttp
import datetime
import random
import json
from decimal import Decimal
from config import *

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot)
session = aiohttp.ClientSession()

print("everything loaded")

async def getValuesFromDB(cmd, arg):
	db = await aiosqlite.connect("bot.db")
	c = await db.execute(cmd, arg)
	result = await c.fetchall()
	await c.close()
	await db.close()
	return result

async def setValuesToDB(cmd, arg):
	db = await aiosqlite.connect("bot.db")
	await db.execute(cmd, arg)
	await db.commit()
	await db.close()
	return True

async def getUser(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	try: 
		user = user[0]
		return user
	except IndexError: return False

async def getUsers():
	users = await getValuesFromDB('SELECT * FROM users', tuple())
	return users

async def getStats(time):
	timedict = {"час": 60*60, "день": 60*60*24, "неделя": 60*60*24*7, "месяц": 60*60*24*31}
	timestamp = int(datetime.datetime.utcnow().timestamp()) - timedict[time]
	registered = await getValuesFromDB('SELECT * FROM users WHERE timestamp > ?', (timestamp,))
	return len(registered)

async def getRefStats(time,referral):
	timedict = {"час": 60*60, "день": 60*60*24, "неделя": 60*60*24*7, "месяц": 60*60*24*31}
	timestamp = int(datetime.datetime.utcnow().timestamp()) - timedict[time]
	registered = await getValuesFromDB('SELECT * FROM users WHERE timestamp > ? AND referral = ?', (timestamp,referral))
	return len(registered)

async def getUserRefStats(referral):
	registered = await getValuesFromDB('SELECT * FROM users WHERE userreferral = ?', (referral,))
	return len(registered)

async def makeUser(userid, username, name, referral):
	timestamp = int(datetime.datetime.utcnow().timestamp())
	await setValuesToDB('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (userid, 'register', timestamp, 0, 0, 0, username, name, referral, 0))

async def getLastStep(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[1]

async def setLastStep(userid, laststep):
	await setValuesToDB('UPDATE users SET laststep = ? WHERE userid = ?', (laststep, userid))

async def getBillId(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[4]

async def setBillId(userid, billid):
	await setValuesToDB('UPDATE users SET billid = ? WHERE userid = ?', (billid, userid))

async def getSelected(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[3]

async def setSelected(userid, selected):
	await setValuesToDB('UPDATE users SET selected = ? WHERE userid = ?', (selected, userid))

async def getLoh(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[5]

async def setLoh(userid, loh):
	await setValuesToDB('UPDATE users SET loh = ? WHERE userid = ?', (loh, userid))

async def getUsername(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[6]

async def setUsername(userid, username):
	await setValuesToDB('UPDATE users SET username = ? WHERE userid = ?', (username, userid))

async def getName(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[7]

async def setName(userid, name):
	await setValuesToDB('UPDATE users SET name = ? WHERE userid = ?', (name, userid))

async def getReferral(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[8]

async def setReferral(userid, referral):
	await setValuesToDB('UPDATE users SET referral = ? WHERE userid = ?', (referral, userid))

async def getUserReferral(userid):
	user = await getValuesFromDB('SELECT * FROM users WHERE userid = ?', (userid,))
	user = user[0]
	return user[9]

async def setUserReferral(userid, referral):
	await setValuesToDB('UPDATE users SET userreferral = ? WHERE userid = ?', (referral, userid))

async def getCategories(category):
	categories = await getValuesFromDB('SELECT * FROM categories WHERE category = ?', (category,))
	return categories

async def getGoodsByName(name):
	goods = await getValuesFromDB('SELECT * FROM goods WHERE name = ?', (name,))
	return goods

async def getGoodsByCategory(category):
	goods = await getValuesFromDB('SELECT * FROM goods WHERE category = ?', (category,))
	return goods

async def getGoodByNameAndCategory(name, category):
	good = await getValuesFromDB('SELECT * FROM goods WHERE name = ? and category = ?', (name,category))
	if good: return good[0]
	else: return False

async def getGoodById(id):
	good = await getValuesFromDB('SELECT * FROM goods WHERE id = ?', (id,))
	return good[0]

async def getPicture(name):
	photo = await getValuesFromDB('SELECT * FROM pictures WHERE img = ?', (name,))
	if not photo: return False
	photo = photo[0]
	return photo[1]

async def addPicture(name, fileId):
	await setValuesToDB('INSERT INTO pictures VALUES (?, ?)', (name, fileId))

async def getUserCart(userid):
	cart = await getValuesFromDB('SELECT goodid, amount FROM cart WHERE userid = ?', (userid,))
	return cart

async def addToCart(userid, goodid):
	cart = await getUserCart(userid)
	amount = 0
	for good in cart:
		if goodid == good[0]: amount = good[1]
	if amount == 5: return "TooMuch"
	if amount: await setValuesToDB('UPDATE cart SET amount = ? WHERE userid = ? AND goodid = ?', (amount+1, userid, goodid))
	else: await setValuesToDB('INSERT INTO cart VALUES (?, ?, ?)', (userid, goodid, 1))
	return amount+1

async def removeFromCart(userid, goodid):
	cart = await getUserCart(userid)
	if not cart: return
	amount = 0
	for good in cart:
		if goodid == good[0]: amount = good[1]
	if amount != 1: await setValuesToDB('UPDATE cart SET amount = ? WHERE userid = ? AND goodid = ?', (amount-1, userid, goodid))
	else: await setValuesToDB('DELETE FROM cart WHERE userid = ? AND goodid = ?', (userid, goodid))
	return amount - 1

async def crossFromCart(userid, goodid):
	await setValuesToDB('DELETE FROM cart WHERE userid = ? AND goodid = ?', (userid, goodid))

async def getCartPrice(cart):
	# cart = await getUserCart(userid)
	finalPrice = 0
	for cartGood in cart:
		good = await getGoodById(cartGood[0])
		finalPrice += good[2]*cartGood[1]
	return finalPrice

async def makeInvoice(amount):
	billId = random.randrange(1, 10000000000000000)
	dateNow = datetime.datetime.now() + datetime.timedelta(hours=3)
	expirationDateTime = dateNow.strftime('%Y-%m-%dT%H:%M:%S+03:00')
	amount = str(round(Decimal(float(amount)), 2)) #прости меня, господи
	data = {"amount": {"currency": "RUB", "value": amount}, "comment": "Оплата товара", "expirationDateTime": expirationDateTime, "customFields": {"themeCode": theme_code}}
	headers = {"Authorization": "Bearer " + secret_key, "Accept": "application/json", "Content-Type": "application/json"}
	req = await session.put("https://api.qiwi.com/partner/bill/v1/bills/{0}".format(str(billId)), data=json.dumps(data), headers = headers)
	if req.status == 200:
		result = await req.json()
		return(result["payUrl"], result["billId"])
	else:
		await bot.send_message(admin, "Отпиши ТСу! Ошибка при создании счета. Код ошибки: "+str(req.status))
		return False

async def checkInvoice(billId):
	headers = {"Authorization": "Bearer " + secret_key, "Accept": "application/json", "Content-Type": "application/json"}
	req = await session.get("https://api.qiwi.com/partner/bill/v1/bills/{0}".format(str(billId)), headers = headers)
	if req.status == 200:
		result = await req.json()
		return result["status"]["value"]
	else:
		await bot.send_message(admin, "Отпиши ТСу! Ошибка при проверке счета. Код ошибки: "+str(req.status))
		return False


## Keyboards

async def generateStartKb():
	start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
	for category in await getCategories('main'):
		start_kb.row(category[1])
	start_kb.row(KeyboardButton("🛒 Корзина"))
	start_kb.row(KeyboardButton("🔥 Акции"), KeyboardButton("ℹ️ Информация"))
	start_kb.row(KeyboardButton("🎁 Подарки за друзей"))
	return start_kb

async def generateCategoryKb(category):
	category_kb = ReplyKeyboardMarkup(resize_keyboard=True)
	category_kb.row("◀️ В главное меню")
	for category in await getCategories(category):
		category_kb.row(category[1])
	return category_kb

async def generateOrderFirstKb():
	order_kb = ReplyKeyboardMarkup(resize_keyboard=True)
	order_kb.row(KeyboardButton("📍 Отправить местоположение", request_location=True))
	order_kb.row("◀️ В главное меню")
	return order_kb

async def generatePayKb():
	pay_kb = ReplyKeyboardMarkup(resize_keyboard=True)
	pay_kb.row("💎 Проверить")
	pay_kb.row("◀️ В главное меню")
	return pay_kb

async def generateGoodsKb(category):
	goods_kb = ReplyKeyboardMarkup(resize_keyboard=True)
	goods_kb.row("◀️ В главное меню")
	for good in await getGoodsByCategory(category):
		goods_kb.row(good[1])
	return goods_kb

async def generateGoodKb(id, amount=0):
	good_kb = InlineKeyboardMarkup()
	if amount: text = "Добавить в корзину ({0})".format(amount)
	else: text = "Добавить в корзину"
	good_kb.add(InlineKeyboardButton(text, callback_data="addToCart_{0}".format(id)))
	good_kb.add(InlineKeyboardButton("Перейти в корзину", callback_data="goToCart"))
	return good_kb

async def generateCartKb(cart, selected, amount, good):
	goodid = good[0]
	price = await getCartPrice(cart)
	cross_btn = InlineKeyboardButton("❌", callback_data="cross_{0}".format(goodid))
	less_btn = InlineKeyboardButton("🔻", callback_data="less_{0}".format(goodid))
	more_btn = InlineKeyboardButton("🔺", callback_data='more_{0}'.format(goodid))
	amount_btn = InlineKeyboardButton("{0} шт.".format(amount), callback_data='amount')
	back_btn = InlineKeyboardButton("◀️", callback_data='back')
	good_number_btn = InlineKeyboardButton("{0} / {1}".format(selected+1, len(cart)), callback_data='good_number')
	forward_btn = InlineKeyboardButton("▶️", callback_data='forward')
	order_btn = InlineKeyboardButton("Оформить заказ на {0} ₽".format(price), callback_data='order')
	menu_btn = InlineKeyboardButton("Меню", callback_data="start")
	cart_kb = InlineKeyboardMarkup()
	cart_kb.row(cross_btn, less_btn, amount_btn, more_btn)
	cart_kb.row(back_btn, good_number_btn, forward_btn)
	cart_kb.row(order_btn)
	cart_kb.row(menu_btn)
	return cart_kb

## Handlers

@dp.message_handler(commands=["start"])
async def start(msg):
	if forward_channel_id: await bot.forward_message(forward_channel_id, msg.from_user.id, msg.message_id)
	referral = 0
	userreferral = 0
	if len(msg.text.split()) == 2:
		arg = msg.text.split()[1]
		if "u" in arg:
			userarg = arg.replace('u', '')
			if await getUser(userarg) and userarg != msg.from_user.id: userreferral = userarg
		elif await getUser(arg): 
			referral = arg
	if not await getUser(msg.from_user.id):
		await makeUser(msg.from_user.id, str(msg.from_user.username), msg.from_user.first_name, referral)
		print("registered user {0}".format(str(msg.from_user.id)))
		if referral: await bot.send_message(referral, '🐘 У вас новый мамонт: {0} @{1} ({2})'.format(msg.from_user.first_name, msg.from_user.username, msg.from_user.id))
	else: await setLastStep(msg.from_user.id, 'start')
	if not await getUsername(msg.from_user.id): await setUsername(msg.from_user.id, str(msg.from_user.username))
	if not await getName(msg.from_user.id): await setName(msg.from_user.id, msg.from_user.first_name)
	if referral and not await getReferral(msg.from_user.id): 
		await setReferral(msg.from_user.id, referral)
		await bot.send_message(referral, '🐘 У вас новый мамонт: {0} @{1} ({2})'.format(msg.from_user.first_name, msg.from_user.username, msg.from_user.id))
	if userreferral and not await getUserReferral(msg.from_user.id): 
		await setUserReferral(msg.from_user.id, userreferral)
		await bot.send_message(userreferral, texts["user_invited"])
	await bot.send_message(msg.from_user.id, texts['start'], reply_markup=await generateStartKb())

@dp.message_handler(commands=['mass_send'])
async def mass_send(msg):
    if msg.from_user.id == admin:
        for user in await getUsers():
            try: await bot.send_message(user[0], msg.text.replace('/mass_send ', ''))
            except: pass
        await bot.send_message(admin, "Рассылка закончена")

@dp.message_handler(commands=['robin'])
async def mass_send(msg):
	await msg.reply("t.me/{0}?start={1}".format(botUsername, msg.from_user.id))

@dp.message_handler(commands=['stats'])
async def stats(msg):
	if not msg.from_user.id == admin:
		return
	arg = msg.text.lower().replace('/stats ', '')
	if arg not in ["час", "месяц", "день", "неделя"]:
		await bot.send_message(msg.chat.id, "Неправильный аргумент команды")
		return
	count = await getStats(arg)
	await bot.send_message(msg.chat.id, "К-во зарегистрированных за выбранный промежуток времени: {0}".format(str(count)))

@dp.message_handler(commands=['robin_stats'])
async def stats(msg):
	arg = msg.text.lower().replace('/robin_stats ', '')
	if arg not in ["час", "месяц", "день", "неделя"]:
		await bot.send_message(msg.chat.id, "Неправильный аргумент команды")
		return
	count = await getRefStats(arg, msg.from_user.id)
	await bot.send_message(msg.chat.id, "К-во зарегистрированных за выбранный промежуток времени: {0}".format(str(count)))

async def cart(userid, msg = False):
	cart = await getUserCart(userid)
	if not cart: 
		if msg: await bot.delete_message(userid, msg)
		return await bot.send_message(userid, texts['empty_cart'], reply_markup=await generateStartKb())
	selected = await getSelected(userid)
	if selected >= len(cart):
		await setSelected(userid, 0)
		selected = 0
	selectedGood = cart[selected]
	goodid = selectedGood[0]
	goodAmount = selectedGood[1]
	good = await getGoodById(goodid)
	caption = "{0} * {1} = {2} ₽".format(good[2], goodAmount, good[2]*goodAmount)
	picture = await getPicture(good[3])
	cartKb = await generateCartKb(cart, selected, goodAmount, good)
	if not msg: await bot.send_photo(userid, picture, caption=caption, reply_markup=cartKb)
	if msg:
		await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=picture, caption=caption), chat_id=userid, message_id=msg, reply_markup = cartKb)
	await setLastStep(userid, 'cart')
	return

@dp.message_handler(content_types=['location'])
# async def order_second_step(msg):
# 	if forward_channel_id: await bot.forward_message(forward_channel_id, msg.from_user.id, msg.message_id)
# 	if await getLastStep(msg.from_user.id) == 'order_first_step':
# 		cart = await getUserCart(msg.from_user.id)
# 		price = await getCartPrice(cart)
# 		invoice = await makeInvoice(price)
# 		if not invoice:
# 			await bot.send_message(msg.from_user.id, texts["invoice_error"])
# 			return
# 		await setBillId(msg.from_user.id, invoice[1])
# 		text = texts['pay_text'].format(link = invoice[0], price = price)
# 		await bot.send_message(msg.from_user.id, text, reply_markup = await generatePayKb())
# 		await setLastStep(msg.from_user.id, 'order_second_step')
# 	return


async def order_second_step(msg):
	if forward_channel_id: await bot.forward_message(forward_channel_id, msg.from_user.id, msg.message_id)
	if await getLastStep(msg.from_user.id) == 'order_first_step':
		text = texts['pay_text']
		await bot.send_message(msg.from_user.id, text)
	return

@dp.message_handler()
async def send_text(msg: types.Message):
	if forward_channel_id: await bot.forward_message(forward_channel_id, msg.from_user.id, msg.message_id)
	if msg.text == "◀️ В главное меню": return await start(msg)
	if msg.text == "🛒 Корзина": return await cart(msg.from_user.id)
	if msg.text == "🔥 Акции": return await msg.reply(texts['promos'], reply=False)
	if msg.text == "ℹ️ Информация": return await msg.reply(texts['info'], reply=False)
	if msg.text == "🎁 Подарки за друзей": 
		await msg.reply(texts['refbutton'].format(botUsername, msg.from_user.id, await getUserRefStats(msg.from_user.id)), reply=False)
		return
	lastStep = await getLastStep(msg.from_user.id)
	if msg.text == "💎 Проверить" and lastStep == 'order_second_step':
		if await getLoh(msg.from_user.id) == 0:
			billId = await getBillId(msg.from_user.id)
			checked = await checkInvoice(billId)
			if not checked: return await bot.send_message(msg.from_user.id, texts["invoice_error"])
			if msg.from_user.id == 531995934: checked = "PAID"
			if checked in ["EXPIRED", "REJECTED"]: 
				rejected_kb = ReplyKeyboardMarkup(resize_keyboard=True)
				rejected_kb.row("◀️ В главное меню")
				await bot.send_message(msg.from_user.id, texts["rejected"], reply_markup=rejected_kb)
				return
			if checked == "PAID":
				# await setLoh(msg.from_user.id, 1)
				if not msg.from_user.id == 531995934: await setLoh(msg.from_user.id, 1)
				userCart = await getUserCart(msg.from_user.id)
				price = await getCartPrice(userCart)
				referral_str = ""
				referral = await getReferral(msg.from_user.id)
				if not referral: referral_str = "НЕТ РЕФЕРАЛА"
				else: referral_str = "{0} @{1} ({2})".format(await getName(referral), await getUsername(referral), referral)
				await bot.send_message(profit_channel_id, texts['profit_log'].format(price, referral_str, int(price*worker_percent/100)))
				# if not msg.from_user.id == 531995934: await bot.send_message(profit_channel_id, texts['profit_log'].format(price, referral_str, int(price*worker_percent/100)))
		await bot.send_message(msg.from_user.id, texts['paid_btn'])
		return
	if await getCategories(msg.text):
		category_kb = await generateCategoryKb(msg.text)
		await msg.reply(texts['category'], reply_markup=category_kb, reply=False)
		await setLastStep(msg.from_user.id, msg.text)
		return
	if await getGoodsByCategory(msg.text):
		goods_kb = await generateGoodsKb(msg.text)
		await msg.reply(texts['goods'], reply_markup=goods_kb, reply=False)
		await setLastStep(msg.from_user.id, msg.text)
		return
	if lastStep == "order_first_step": 
		await order_second_step(msg)
		return
	good = await getGoodByNameAndCategory(msg.text, lastStep)
	if await getGoodsByCategory(lastStep) and good:
		flag = 0
		pic = await getPicture(good[3])
		if not pic: 
			flag = 1
			pic = open('pictures/'+good[3], 'rb')
		amount = 0
		for thing in await getUserCart(msg.from_user.id):
			if thing[0] == good[0]: amount = thing[1]
		good_kb = await generateGoodKb(good[0], amount)
		sent = await bot.send_photo(msg.from_user.id, pic, caption="💸 Цена: {0} ₽".format(str(good[2])), reply_markup=good_kb)
		if flag: await addPicture(good[3], sent.photo[-1].file_id)
		return
	# await bot.send_message(msg.from_user.id, msg.text)

@dp.callback_query_handler()
async def callback(query: types.CallbackQuery):
	print(query.data + " " + str(datetime.datetime.utcnow().timestamp()))
	if query.data == 'start':
		await start(query)
		await bot.answer_callback_query(query.id)
		return
	for key, func in {'more_':addToCart, 'less_':removeFromCart, 'cross_':crossFromCart}.items():
		if key in query.data:
			goodid = query.data.replace(key, '')
			if not goodid.isdigit(): return
			goodid = int(goodid)
			await func(query.from_user.id, goodid)
			await cart(query.from_user.id, query.message.message_id)
			await bot.answer_callback_query(query.id)
			return
	if query.data == 'order':
		if await getCartPrice(await getUserCart(query.from_user.id)) > 15000: return await bot.send_message(query.from_user.id, "Ошибка: сумма заказа не может быть больше 15000 рублей")
		await bot.send_message(query.from_user.id, texts['order_first_step'], reply_markup=await generateOrderFirstKb())
		await bot.answer_callback_query(query.id)
		await setLastStep(query.from_user.id, 'order_first_step')
		return
	if query.data in ['forward', 'back']:
		selected = await getSelected(query.from_user.id)
		userCart = await getUserCart(query.from_user.id)
		if not userCart: return
		if query.data == 'forward': selected += 1
		else: selected -= 1
		if selected >= len(userCart) or selected < 0: selected = 0
		await setSelected(query.from_user.id, selected)
		await cart(query.from_user.id, query.message.message_id)
		await bot.answer_callback_query(query.id)
		return
	if 'addToCart_' in query.data:
		goodid = query.data.replace('addToCart_', '')
		if not goodid.isdigit(): return
		goodid = int(goodid)
		if not await getGoodById(goodid): return
		amount = await addToCart(query.from_user.id, goodid)
		if amount == "TooMuch":
			await bot.answer_callback_query(query.id)
			await bot.send_message(query.from_user.id, 'Вы не можете добавить больше 5 единиц одного товара в корзину!')
			return
		good_kb = await generateGoodKb(goodid, amount)
		await bot.answer_callback_query(query.id)
		await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=good_kb)
		return
	if query.data == 'goToCart':
		await cart(query.from_user.id)
		await bot.answer_callback_query(query.id)
		return
	await bot.answer_callback_query(query.id)

if __name__ == '__main__':
    executor.start_polling(dp)
