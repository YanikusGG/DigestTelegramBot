import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN, DEFAULT_CHANNELS, DEFAULT_POSTS_LIMIT, DEFAULT_PERIOD, MAX_REQUESTS_PER_CHANNEL
from main import keyboard_start, dp, Digest

from bs4 import BeautifulSoup
from datetime import timedelta, datetime, timezone
import re
import requests


def get_channels(): #TODO
    return DEFAULT_CHANNELS

def get_posts_limit(): #TODO
    return DEFAULT_POSTS_LIMIT

def get_period(): #TODO
    return DEFAULT_PERIOD


async def get_last_image_id(channel):
    channel_url = f'https://t.me/s/{channel}'
    req = requests.get(channel_url)
    soup = BeautifulSoup(req.content.decode("utf-8"), 'html.parser')
    images = soup.find_all('a', {'class': 'tgme_widget_message_photo_wrap'})
    hrefs = [image.get('href')[len(channel_url)-1:] for image in images]
    return max(int(href[:-7] if href[-7:] == '?single' else href) for href in hrefs)

async def parse_image(channel, image_id):
    req = requests.get(f'https://t.me/s/{channel}/{image_id}')
    soup = BeautifulSoup(req.content.decode("utf-8"), 'html.parser')
    image = soup.find('a', {'class': 'tgme_widget_message_photo_wrap', 'href': f'https://t.me/{channel}/{image_id}'}) or \
            soup.find('a', {'class': 'tgme_widget_message_photo_wrap', 'href': f'https://t.me/{channel}/{image_id}?single'})
    if image is None:
        return None, None
    url = re.match(r".*background-image:url\('(.*?)'\).*", image.get('style')).group(1)
    if image.get('href')[-7:] == '?single':
        time = image.parent.parent.parent.parent.find('time')
    else:
        time = image.parent.find('time')
    dt = datetime.fromisoformat(time.get('datetime')).replace(tzinfo=timezone.utc)
    return url, dt

async def get_images_from_channel(channel):
    posts_limit = get_posts_limit()
    period = get_period()

    res_images = []
    now = datetime.now(tz=timezone.utc)
    image_id = await get_last_image_id(channel)
    request_count = 0

    while image_id > 0 and request_count < MAX_REQUESTS_PER_CHANNEL and (len(res_images) < posts_limit or posts_limit == -1):
        url, dt = await parse_image(channel, image_id)
        image_id -= 1
        request_count += 1
        if url is None:
            continue
        if dt + period < now:
            break
        res_images.append(url)
    return res_images

@dp.message_handler(Text(["Получить мой дайджест!"]), state=Digest.confirm_digest)
async def send_digest(message: types.Message, state: FSMContext):
    channels = get_channels()

    await message.answer("Лови Дайджест!")
    for channel in channels:
        images = await get_images_from_channel(channel)
        if images:
            await message.answer(f"Мемы из канала @{channel}:")
            media = [types.input_media.InputMediaPhoto(media=image) for image in images]
            offset = 0
            while offset < len(media):
                await message.answer_media_group(types.input_media.MediaGroup(media[offset:offset+10]))
                offset += 10
    await Digest.confirm_digest.set()
