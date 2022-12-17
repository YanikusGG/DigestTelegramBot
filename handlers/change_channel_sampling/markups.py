from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_CHANNELS
from db import connector


def create_menu(array):
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(len(DEFAULT_CHANNELS)):
        prefix = '-'
        if DEFAULT_CHANNELS[i] in array:
            prefix = '✅'
        menu.insert(InlineKeyboardButton(text=f"{prefix} {DEFAULT_CHANNELS[i]}",
                                         callback_data='-_-' + DEFAULT_CHANNELS[i]))
    menu.insert(InlineKeyboardButton(text="Добавить свой канал",
                                     callback_data='Add own channel'))
    menu.insert(InlineKeyboardButton(text="Убрать канал из выборки",
                                     callback_data='Remove channel'))
    return menu


def create_menu_global(channel, user_id):
    connector.init_db()
    row = connector.get_row(user_id)
    connector.close_db()
    if not row:
        return False
    channels = decode_string(row[1])
    channel = channel[3:]
    if channel not in DEFAULT_CHANNELS:
        return create_menu(channels)

    if channel in channels:
        channels.remove(channel)
    else:
        channels.append(channel)
    connector.init_db()
    connector.update_channels(user_id, encode_array(channels))
    connector.close_db()
    return create_menu(channels)


def add_custom_channel(channel, user_id):
    connector.init_db()
    row = connector.get_row(user_id)
    connector.close_db()
    if not row:
        return False
    channels = decode_string(row[1])
    if channel in channels:
        return True
    channels.append(channel)
    connector.init_db()
    connector.update_channels(user_id, encode_array(channels))
    connector.close_db()
    return True


def remove_custom_channel(channel, user_id):
    connector.init_db()
    row = connector.get_row(user_id)
    connector.close_db()
    if not row:
        return False
    channels = decode_string(row[1])
    if channel not in channels:
        return False
    channels.remove(channel)
    connector.init_db()
    connector.update_channels(user_id, encode_array(channels))
    connector.close_db()
    return True


def encode_array(array):
    encoded_str = ''
    for i in range(len(array)):
        encoded_str += array[i]
        if i < len(array) - 1:
            encoded_str += '-_-'
    return encoded_str


def decode_string(arr_string=str):
    if arr_string == '':
        return []
    array = arr_string.split('-_-')
    return array
