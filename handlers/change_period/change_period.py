﻿import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN
from main import keyboard_start, dp, Digest


@dp.message_handler(Text(["Изменить период"]), state=Digest.confirm_digest)
async def change_period(message: types.Message, state: FSMContext):
    # TODO
    # тут типа отправить сообщение выбери период
    await Digest.change_period.set()