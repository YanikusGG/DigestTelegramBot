import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN
from main import keyboard_parameters, dp, Digest
import re

DEFAULT_POSTS_LIMIT = 10


async def set_default_limit(x):
    global DEFAULT_POSTS_LIMIT
    DEFAULT_POSTS_LIMIT = x


@dp.message_handler(Text(["Изменить ограничение на количество записей"]), state=Digest.confirm_digest)
async def change_posts_limit(message: types.Message, state: FSMContext):
    but_10 = [types.KeyboardButton(text="10 записей")]
    but_20 = [types.KeyboardButton(text="20 записей")]
    but_50 = [types.KeyboardButton(text="50 записей")]
    but_own = [types.KeyboardButton(text="Свое ограничение на записи")]
    but_off = [types.KeyboardButton(text="Снять ограничение")]
    kb_options = [but_10, but_20, but_50, but_own, but_off]
    keyboard_posts_limits = types.ReplyKeyboardMarkup(keyboard=kb_options, resize_keyboard=True)
    await Digest.change_posts_limit.set()
    await message.answer("Выбери ограничение на количество записей!", reply_markup=keyboard_posts_limits)


@dp.message_handler(Text(endswith = "записей"), state=Digest.change_posts_limit)
async def set_definite_posts_limit(message: types.Message, state: FSMContext):
    num = int(re.search(r'\d+', message.text).group(0))
    await set_default_limit(num)
    await Digest.confirm_digest.set()
    await message.answer(f"Поменял ограничение на: {message.text}", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Снять ограничение"]), state=Digest.change_posts_limit)
async def remove_limit(message: types.Message, state: FSMContext):
    await set_default_limit(-1)
    await Digest.confirm_digest.set()
    await message.answer("Снял ограничение на количество записей", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Свое ограничение на записи"]), state=Digest.change_posts_limit)
async def get_own_posts_limit(message: types.Message, state: FSMContext):
    await message.answer("Введи свое ограничение на записи")


@dp.message_handler(Text, state=Digest.change_posts_limit)
async def set_own_posts_limit(message: types.Message, state: FSMContext):
    num = int(re.search(r'\d+', message.text).group(0))
    await set_default_limit(num)
    await Digest.confirm_digest.set()
    await message.answer(f"Изменил ограничение на записи: {num} записей", reply_markup=keyboard_parameters)

