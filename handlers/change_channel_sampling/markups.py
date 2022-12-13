from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_CHANNELS
from db import connector


def create_menu(array):
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(8):
        prefix = '-'
        if DEFAULT_CHANNELS[i] in array:
            prefix = '✅'
        menu.insert(InlineKeyboardButton(text=f"{prefix} {DEFAULT_CHANNELS[i]}",
                                         callback_data='-_-' + DEFAULT_CHANNELS[i]))
    return menu


def create_menu_global(callback, user_id):
    connector.init_db()
    row = connector.get_row(user_id)
    connector.close_db()
    if not row:
        return False
    channels_str = row[1]
    channels = decode_string(channels_str)
    callback = callback[3:]
    if callback not in DEFAULT_CHANNELS:
        return create_menu(channels)

    if callback in channels:
        channels.remove(callback)
    else:
        channels.append(callback)
    connector.init_db()
    connector.update_channels(user_id, encode_array(channels))
    connector.close_db()
    return create_menu(channels)


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
