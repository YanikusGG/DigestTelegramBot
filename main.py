import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN

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
    [types.KeyboardButton(text="Изменить выборку каналов")],
    [types.KeyboardButton(text="Изменить период")],
    [types.KeyboardButton(text="Изменить ограничение на количество записей")],
    [types.KeyboardButton(text="Получить мой дайджест!")],
]
keyboard_parameters = types.ReplyKeyboardMarkup(keyboard=kb_parameters,
                                                resize_keyboard=True)


class Digest(StatesGroup):
    confirm_digest = State()
    change_channel_sampling = State()
    change_period = State()
    change_posts_limit = State()


@dp.message_handler(Text(["Что ты умеешь делать?"]))
async def start(message: types.Message):
    await message.answer("Я умею присылать дайджесты по мемам!)", reply_markup=keyboard_start)


@dp.message_handler(Text(["Дайджест"]))
async def start_digest(message: types.Message):
    await Digest.confirm_digest.set()
    await message.answer("Я автоматически собираю мемы со всех каналов за последние сутки. Текущие параметры: ...\n\n"
                         "Если хочешь поменять параметры - вперед!)", reply_markup=keyboard_parameters)


@dp.message_handler(commands=['start', 'info'])
async def send_welcome(message: types.Message):
    await message.answer("Привет, " + message.chat.username + "🥰\n" +
                         "Я не просто бот, я истинный ценитель мемов!!",
                         reply_markup=keyboard_start)


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
