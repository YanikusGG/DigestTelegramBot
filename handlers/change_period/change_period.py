import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN as API_TOKEN
from main import keyboard_parameters, dp, Digest
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from datetime import  timedelta, datetime


DEFAULT_PERIOD = timedelta(days=1)

async def set_default_period(x):
    global DEFAULT_PERIOD
    DEFAULT_PERIOD = x

@dp.message_handler(Text(["Изменить период"]), state=Digest.confirm_digest)
async def change_period(message: types.Message, state: FSMContext):
    but_day = [types.KeyboardButton(text="День")]
    but_hour = [types.KeyboardButton(text="Неделя")]
    but_month = [types.KeyboardButton(text="Месяц")]
    but_own = [types.KeyboardButton(text="Свой период")]
    kb_options = [but_hour, but_day, but_month, but_own]
    keyboard_period = types.ReplyKeyboardMarkup(keyboard=kb_options, resize_keyboard=True)
    await Digest.change_period.set()
    await message.answer("Выбери период!", reply_markup=keyboard_period)


@dp.message_handler(Text(["День"]), state=Digest.change_period)
async def change_period(message: types.Message, state: FSMContext):
    await set_default_period(timedelta(days=1))
    await Digest.confirm_digest.set()
    await message.answer("Период изменен на: 1 день", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Неделя"]), state=Digest.change_period)
async def change_period(message: types.Message, state: FSMContext):
    await set_default_period(timedelta(days=7))
    await Digest.confirm_digest.set()
    await message.answer("Период изменен на: 7 дней", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Месяц"]), state=Digest.change_period)
async def change_period(message: types.Message, state: FSMContext):
    await set_default_period(timedelta(days=30))
    await Digest.confirm_digest.set()
    await message.answer("Период изменен на: 30 дней", reply_markup=keyboard_parameters)


@dp.message_handler(Text(["Свой период"]), state=Digest.change_period)
async def change_period(message: types.Message, state: FSMContext):
    await message.answer("Выбери дату начала", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=Digest.change_period)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, selected_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        if selected_date > datetime.now():
            await callback_query.message.answer("Ты неверно задал дату(((")
        else:
            period = datetime.now() - selected_date
            await set_default_period(timedelta(days=period.days))
            days_string = "дней"
            if period.days % 10 == 1:
                days_string = "день"
            elif period.days % 10 in [2, 3, 4]:
                days_string = "дня"
            await Digest.confirm_digest.set()
            await callback_query.message.answer(f'Изменил период на: {period.days} {days_string}',
                                                reply_markup=keyboard_parameters)

