from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from logging.handlers import QueueHandler
from config import TOKEN as API_TOKEN
from markups import make_me, array_with_chanels
from main import keyboard_start, dp, Digest, bot


@dp.message_handler(Text(["Изменить выборку каналов"]), state=Digest.confirm_digest)
async def change_channel_sampling(callback: QueueHandler):
    to = callback.from_user.id
    await bot.send_message(to, 'Выберите ваш канал', reply_markup=make_me('', to))


@dp.callback_query_handler(Text(startswith='r'), state=Digest.confirm_digest)
async def check_system(callback: QueueHandler):
    need_to_send = callback.data
    to = callback.from_user.id
    # await bot.delete_message(to, message_id=callback.message.message_id)
    # await bot.send_message(to,'Выберите ваш канал', reply_markup = make_me(need_to_send, to))
    menu = make_me(need_to_send, to)
    array = array_with_chanels(to)

    # print(array)

    await callback.message.edit_text('Выберите ваш канал', reply_markup=menu)


