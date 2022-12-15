import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN
from handlers.get_settings import get_period, get_channels, get_posts_limit

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb_start = [
    [types.KeyboardButton(text="Что ты умеешь делать?")],
    [types.KeyboardButton(text="Дайджест")],
]
keyboard_start = types.ReplyKeyboardMarkup(keyboard=kb_start,
                                           resize_keyboard=True)

kb_parameters = [
    [types.KeyboardButton(text="Текущие параметры"), types.KeyboardButton(text="Изменить выборку каналов")],
    [types.KeyboardButton(text="Изменить период"), types.KeyboardButton(text="Изменить количество мемов")],
    [types.KeyboardButton(text="Получить мой дайджест!")],
]
keyboard_parameters = types.ReplyKeyboardMarkup(keyboard=kb_parameters,
                                                resize_keyboard=True)


class Digest(StatesGroup):
    confirm_digest = State()
    change_channel_sampling = State()
    change_period = State()
    change_posts_limit = State()


@dp.message_handler(Text(["Что ты умеешь делать?"]), state='*')
async def start(message: types.Message):
    await message.answer("Я умею присылать дайджесты по мемам!) При этом учитываю установленные тобой параметры!", reply_markup=keyboard_start)


@dp.message_handler(Text(["Дайджест", "Текущие параметры"]), state='*')
async def start_digest(message: types.Message):
    user_id = message.from_user.id
    await Digest.confirm_digest.set()
    await message.answer("Текущие параметры:\n\n"
                         f"Выбранные каналы: {get_channels(user_id)}\n"
                         f"Период: {get_period(user_id).days} дней\n"
                         f"Количество мемов: {get_posts_limit(user_id)}\n\n"
                         "Если хочешь поменять параметры - вперед!)\n"
                         "Если хочешь получить дайджест - я только за!!)", reply_markup=keyboard_parameters)


@dp.message_handler(commands=['start', 'info'], state='*')
async def send_welcome(message: types.Message):
    await message.answer("Привет, " + message.chat.username + "🥰\n" +
                         "Я не просто бот, я истинный ценитель мемов!!",
                         reply_markup=keyboard_start)


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
