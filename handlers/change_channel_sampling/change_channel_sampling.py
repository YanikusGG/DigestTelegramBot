from aiogram import types
from aiogram.dispatcher.filters import Text
from logging.handlers import QueueHandler
from handlers.change_channel_sampling.markups import create_menu_global, add_custom_channel, remove_custom_channel
from main import dp, Digest, bot, start_digest


@dp.message_handler(Text(["Изменить выборку каналов"]), state=Digest.confirm_digest)
async def change_channel_sampling(callback: QueueHandler):
    user_id = callback.from_user.id
    menu = create_menu_global('', user_id)
    if not menu:
        print('Что-то пошло не так')
        return
    await bot.send_message(user_id, 'Выберите ваш канал', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='-_-'), state=Digest.confirm_digest)
async def check_system(callback: QueueHandler):
    channel = callback.data
    user_id = callback.from_user.id
    menu = create_menu_global(channel, user_id)
    if not menu:
        print('Что-то пошло не так')
        return
    await callback.message.edit_text('Выберите ваш канал', reply_markup=menu)


@dp.callback_query_handler(Text(["Add own channel", "Remove channel"]), state=Digest.confirm_digest)
async def custom_channel_sampling(callback: QueueHandler):
    action = callback.data
    user_id = callback.from_user.id
    if action == 'Add own channel':
        await Digest.add_channel.set()
        await bot.send_message(user_id, 'Введите username телеграмм-канала, который хотите добавить')
    elif action == 'Remove channel':
        await Digest.remove_channel.set()
        await bot.send_message(user_id, 'Введите username телеграмм-канала, который хотите убрать')


@dp.message_handler(state=Digest.add_channel)
async def add_channel(message: types.Message):
    if not add_custom_channel(message.text, message.from_user.id):
        print('Что-то пошло не так')
    await start_digest(message)


@dp.message_handler(state=Digest.remove_channel)
async def remove_channel(message: types.Message):
    if not remove_custom_channel(message.text, message.from_user.id):
        print('Что-то пошло не так')
    await start_digest(message)
