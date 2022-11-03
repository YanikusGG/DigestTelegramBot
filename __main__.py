﻿import telebot
from telebot import types

import config


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton('Что ты умеешь?')
    item_2 = types.KeyboardButton('Дайджест')
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я не просто бот, я истинный ценитель мемов!!', reply_markup=markup)

@bot.message_handler(content_types=['text', 'emoji'])
def message_reply(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text=='Что ты умеешь?':
        item_2 = types.KeyboardButton('Дайджест')
        markup.add(item_2)
        bot.send_message(message.chat.id, 'Я умею присылать дайджесты по мемам!)', reply_markup=markup)
    elif message.text == 'Дайджест':
        item_1 = types.KeyboardButton('Что ты умеешь?')
        markup.add(item_1)
        bot.send_message(message.chat.id, 'Упс... функция в процессе разработки', reply_markup=markup)

bot.polling(none_stop=True, interval=0)
