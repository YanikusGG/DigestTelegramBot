from aiogram import types
from aiogram.dispatcher.filters import Text
from main import keyboard_parameters, dp, Digest
import re
from db import connector


async def set_default_limit(user_id, x):
    connector.init_db()
    connector.update_posts_limit(user_id, x)
    connector.close_db()


@dp.message_handler(Text(["Изменить количество мемов"]), state=Digest.confirm_digest)
async def change_posts_limit(message: types.Message):
    but_10 = [types.KeyboardButton(text="10 мемов")]
    but_20 = [types.KeyboardButton(text="20 мемов")]
    but_50 = [types.KeyboardButton(text="50 мемов")]
    but_own = [types.KeyboardButton(text="Свое ограничение на мемы")]
    but_off = [types.KeyboardButton(text="Снять ограничение")]
    kb_options = [but_10, but_20, but_50, but_own, but_off]
    keyboard_posts_limits = types.ReplyKeyboardMarkup(keyboard=kb_options, resize_keyboard=True)
    await Digest.change_posts_limit.set()
    await message.answer("Выбери ограничение на количество мемов!", reply_markup=keyboard_posts_limits)


@dp.message_handler(Text(endswith = "мемов"), state=Digest.change_posts_limit)
async def set_definite_posts_limit(message: types.Message):
    num = int(re.search(r'\d+', message.text).group(0))
    await set_default_limit(message.from_user.id, num)
    await Digest.confirm_digest.set()
    await message.answer(f"Поменял ограничение на: {message.text}", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Снять ограничение"]), state=Digest.change_posts_limit)
async def remove_limit(message: types.Message):
    await set_default_limit(message.from_user.id, -1)
    await Digest.confirm_digest.set()
    await message.answer("Снял ограничение на количество мемов", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Свое ограничение на мемы"]), state=Digest.change_posts_limit)
async def get_own_posts_limit(message: types.Message):
    await message.answer("Введи свое ограничение на количество мемов")


@dp.message_handler(Text, state=Digest.change_posts_limit)
async def set_own_posts_limit(message: types.Message):
    num = int(re.search(r'\d+', message.text).group(0))
    await set_default_limit(message.from_user.id, num)
    await Digest.confirm_digest.set()
    await message.answer(f"Изменил ограничение на мемы: {num}", reply_markup=keyboard_parameters)

