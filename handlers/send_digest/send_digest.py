from cmath import e
from aiogram import types
from aiogram.dispatcher.filters import Text
from config import MAX_REQUESTS_PER_CHANNEL
from main import dp, Digest

from bs4 import BeautifulSoup
from datetime import datetime, timezone
from handlers.get_settings import get_period, get_channels, get_posts_limit
import re
import requests


async def get_last_image_id(channel):
    try:
        channel_url = f'https://t.me/s/{channel}'
        req = requests.get(channel_url)
        soup = BeautifulSoup(req.content.decode("utf-8"), 'html.parser')
        images = soup.find_all('a', {'class': 'tgme_widget_message_photo_wrap'})
        hrefs = [image.get('href')[len(channel_url)-1:] for image in images]
        return max(int(href[:-7] if href[-7:] == '?single' else href) for href in hrefs)
    except Exception as e:
        print(e)
        return 0


async def parse_image(channel, image_id):
    try:
        req = requests.get(f'https://t.me/s/{channel}/{image_id}')
        soup = BeautifulSoup(req.content.decode("utf-8"), 'html.parser')
        image = soup.find('a', {'class': 'tgme_widget_message_photo_wrap', 'href': f'https://t.me/{channel}/{image_id}'}) or \
                soup.find('a', {'class': 'tgme_widget_message_photo_wrap', 'href': f'https://t.me/{channel}/{image_id}?single'})
        if image is None:
            return None, None, None
        url = re.match(r".*background-image:url\('(.*?)'\).*", image.get('style')).group(1)
        if re.match(r".*/N.*", url):
            return None, None, None
        if image.get('href')[-7:] == '?single':
            time = image.parent.parent.parent.parent.find('time')
            text = image.parent.parent.parent.parent.find('div', {'class': 'tgme_widget_message_text'})
        else:
            time = image.parent.find('time')
            text = image.parent.find('div', {'class': 'tgme_widget_message_text'})
        dt = datetime.fromisoformat(time.get('datetime')).replace(tzinfo=timezone.utc)
        txt = None
        if text:
            txt = '\n'.join(text.stripped_strings)
        return url, dt, txt
    except Exception as e:
        print(e)
        return None, None, None


async def get_images_from_channel(user_id, channel):
    try:
        posts_limit = get_posts_limit(user_id)
        period = get_period(user_id)

        res_images = []
        now = datetime.now(tz=timezone.utc)
        image_id = await get_last_image_id(channel)
        request_count = 0

        while image_id > 0 and request_count < MAX_REQUESTS_PER_CHANNEL and (len(res_images) < posts_limit or posts_limit == -1):
            url, dt, txt = await parse_image(channel, image_id)
            post_url = f'https://t.me/{channel}/{image_id}'
            image_id -= 1
            request_count += 1
            if url is None:
                continue
            if dt + period < now:
                break
            if txt:
                caption = txt + '\n' + post_url
            else:
                caption = post_url
            res_images.append((url, caption))
        return res_images
    except Exception as e:
        print(e)
        return []


@dp.message_handler(Text(["Получить мой дайджест!"]), state=Digest.confirm_digest)
async def send_digest(message: types.Message):
    user_id = message.from_user.id
    channels = get_channels(user_id)
    if channels is None or len(channels) == 0:
        await message.answer("Вы не выбрали ни одного канала!")
        return
    await message.answer("Лови Дайджест!")
    for channel in channels:
        images = await get_images_from_channel(user_id, channel)
        if images:
            await message.answer(f"Мемы из канала @{channel}:")
            media = [types.input_media.InputMediaPhoto(media=image[0], caption=image[1]) for image in images]
            offset = 0
            while offset < len(media):
                await message.answer_media_group(types.input_media.MediaGroup(media[offset:offset+10]))
                offset += 10
    await Digest.confirm_digest.set()
