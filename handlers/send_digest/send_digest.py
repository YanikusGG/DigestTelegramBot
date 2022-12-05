import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN
from main import keyboard_start, dp, Digest

from bs4 import BeautifulSoup
from config import DEFAULT_CHANNELS, DEFAULT_POSTS_LIMIT
import re
import requests


async def get_images_from_channel(channel: str):
    res_images = []
    req = requests.get(f'https://t.me/s/{channel}')
    soup = BeautifulSoup(req.content.decode("utf-8"), 'html.parser')
    images = soup.find_all('a')
    for image in images:
        if image.get('class') and image.get('class')[0] == 'tgme_widget_message_photo_wrap':
            url = re.match(r".*background-image:url\('(.*?)'\).*", image.get('style')).group(1)
            res_images.append(url)
    if len(res_images) > DEFAULT_POSTS_LIMIT:
        res_images = res_images[::-1][:DEFAULT_POSTS_LIMIT][::-1]
    return res_images

@dp.message_handler(Text(["Получить мой дайджест!"]), state=Digest.confirm_digest)
async def send_digest(message: types.Message, state: FSMContext):
    await message.answer("Лови Дайджест!")
    for channel in DEFAULT_CHANNELS:
        images = await get_images_from_channel(channel)
        if images:
            await message.answer(f"Мемы из канала @{channel}:")
        for image in images:
            await message.answer_photo(photo=image)
    await state.finish()
