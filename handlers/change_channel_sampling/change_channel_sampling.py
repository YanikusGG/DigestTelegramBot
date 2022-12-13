from aiogram.dispatcher.filters import Text
from logging.handlers import QueueHandler
from handlers.change_channel_sampling.markups import create_menu_global
from main import dp, Digest, bot


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


