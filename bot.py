# -*- coding: utf-8 -*-

# AIOGRAM
from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from random import randrange
from c import check_for_duplicates
import os, random, pathlib
import tinydb

bot_token = '5478961845:AAHqk3NJiVU8s3kMocJM__TsiwWj_dYxDUA'
bot = Bot(token=bot_token)

admin_id = 1218845111
path = 'data/mems/'

db = tinydb.TinyDB('data/db.json')
User = tinydb.Query()

dp = Dispatcher(bot)

async def get_mems_num():
    return len([f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))])

async def get_mem():
    return f'{path}/{random.choice(os.listdir("data/mems/"))}'

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    bot_user = db.search(User.id == message.from_user.id)
    if bot_user == []:
        data = {
            "id": message.from_user.id,
            "mems": 1
        }
        db.insert(data)
    users = len(db.all())

    mems = await get_mems_num()
    mem = await get_mem()

    button_hi = KeyboardButton('➡️')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button_hi)

    await bot.send_photo(
        chat_id=message.chat.id, 
        caption=f'🧑‍💻 <b>Привет дружище, отвлекись и полистай мемы!</b>\n\n 🤣 <i>Всего мемов:</i> <code>~{mems}</code>;\n 🏃 <i>Всего пользователей:</i> <code>~{users}</code>;\n ➕ <i>Добавить мем можно просто отправив его;</i>\n 📌 <i>31 мая в 18:00 из-за ошибки произошёл сброс базы данных.</i>\n\n<i>Made with ❤️ by @vsecoder!</i>', 
        photo=open(mem, 'rb'),
        reply_markup=greet_kb,
        parse_mode='html'
    )

# /delete
@dp.message_handler(commands=['delete'])
async def send_welcome(message: types.Message):
    if message.from_user.id == admin_id:
        try:
            arg = message.text.replace('/delete ', '')
            if arg == '/delete' or arg == '':
                l = check_for_duplicates(path)
                await message.reply(l)
            else:
                os.remove(f'{path}/{arg}.jpg')
                await message.reply(f'Удалено!', parse_mode='html')
        except Exception as e:
            await message.reply(f'{e}')

# /profile
@dp.message_handler(commands=['profile'])
async def send_welcome(message: types.Message):
    bot_user = db.search(User.id == message.from_user.id)

    if bot_user == []:
        return await message.reply(f'😞 Вас нет в базе данных бота, введите /start для продолжения', parse_mode='html')
    bot_user = bot_user[0]

    await message.reply(f'👨‍💻 <b>@{message.from_user.username}</b> <code>{message.from_user.id}</code>\n🤣 <i>Всего мемов просмотрено:</i> <code>~{bot_user["mems"]}</code>', parse_mode='html')

# new mems download
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if message.from_user.id == admin_id:
        name = randrange(1000000000000)
        await message.photo[-1].download(f'{path}/{name}.jpg')
        #await message.reply(f'<code>/mems/{name}.jpg</code> - saved', parse_mode='html')
    else:
        await message.reply(f'😞 Не удалось переслать ваш мем на проверку, попробуйте отправить его @vsecoder\'у', parse_mode='html')

# send mems
@dp.message_handler()
async def hndl_message(message: types.Message):
    bot_user = db.search(User.id == message.from_user.id)

    if bot_user == []:
        return await message.reply(f'😞 Вас нет в базе данных бота, введите /start для продолжения', parse_mode='html')
    bot_user = bot_user[0]
    mems = int(bot_user['mems']) + 1
    db.update({'mems': mems}, User.id == message.from_user.id)

    mem = await get_mem()
    await bot.send_photo(chat_id=message.chat.id, photo=open(mem, 'rb'))

if __name__ == "__main__":
	executor.start_polling(dp)