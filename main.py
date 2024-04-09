import telebot
import time
import random
import os
import currencies
from datetime import datetime

with open('my_token.txt', 'r') as file:
    token = file.readline()

bot = telebot.TeleBot(token)

d = dict()
d2 = dict()

def create_currency(name):
    c = currencies.Currency(name)
    if c.get_name() == None:
        return None
    return c

def create(chat_id, name, dct):
    chat_id = str(chat_id)
    if chat_id not in dct:
        dct[chat_id] = []
        c = create_currency(name)
        if c == None:
            return None
        dct[chat_id].append(c)
    else:
        f = False
        for i in dct[chat_id]:
            if i.check_input_name(name):
                f = True
                break
        if f == False:
            c = create_currency(name)
            if c == None:
                return None
            dct[chat_id].append(c)
    return True


@bot.message_handler(commands=['start'])
def start(message):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == '12:00:00':
            for i in d2[str(message.chat.id)]:
                bot.send_message(message.chat.id, f'Сегодня 1 {i.get_name()} стоит {i.update_value()} рублей.')
            time.sleep(2)

@bot.message_handler(commands=['get_price'])
def course(message):
    bot.send_message(message.chat.id, 'Введите название валюты, цену которой вы хотите получить')
    bot.register_next_step_handler(message, get_currency_name)
def get_currency_name(message):
    if create(message.chat.id, message.text, d) == None:
        bot.send_message(message.chat.id, 'Введите название валюты точнее, пожалуйста')
        bot.register_next_step_handler(message, get_currency_name)
        return
    for i in d[str(message.chat.id)]:
        if i.check_input_name(message.text):
            bot.send_message(message.chat.id, f'{i.get_name()} - {i.update_value()} рублей')
            break

@bot.message_handler(commands=['subscription_currency'])
def subscription(message):
    bot.send_message(message.chat.id, 'Введите название валюты, цену которой вы хотите получать в 12:00 по Москве')
    bot.register_next_step_handler(message, subscription_currency)
def subscription_currency(message):
    if create(message.chat.id, message.text, d2) == None:
        bot.send_message(message.chat.id, 'Введите название валюты точнее, пожалуйста')
        bot.register_next_step_handler(message, subscription_currency)
        return
    for i in d2[str(message.chat.id)]:
        if i.check_input_name(message.text):
            bot.send_message(message.chat.id, f'Вы подписались на {i.get_name()}')
            break

class graph_info:
    x = ''
    y = ''
    date_from = ''
    date_to = ''

@bot.message_handler(commands=['get_graphs'])
def course(message):
    g = graph_info()
    bot.send_message(message.chat.id, 'Введите название валюты, цена которой будет на оси OX')
    bot.register_next_step_handler(message, get_name_x, g)
def get_name_x(message, g):
    if message.text.lower() == 'рубль':
        g.x = 'рубль'
    else:
        g.x = create_currency(message.text)
    if g.x == None:
        bot.send_message(message.chat.id, 'Введите название валюты, точнее, пожалуйста')
        bot.register_next_step_handler(message, get_name_x, g)
    else:
        bot.send_message(message.chat.id, 'Введите название валюты, цена которой будет на оси OY')
        bot.register_next_step_handler(message, get_name_y, g)
def get_name_y(message, g):
    if message.text.lower() == 'рубль':
        g.y = 'рубль'
    else:
        g.y = create_currency(message.text)
    if g.y == None:
        bot.send_message(message.chat.id, 'Введите название валюты, точнее, пожалуйста')
        bot.register_next_step_handler(message, get_name_y, g)
    else:
        bot.send_message(message.chat.id, 'Введите название даты от которой брать цену в формате dd.mm.yyyy')
        bot.register_next_step_handler(message, get_date_from, g)
def get_date_from(message, g):
    g.date_from = message.text
    bot.send_message(message.chat.id, 'Введите название даты до которой брать цену в формате dd.mm.yyyy')
    bot.register_next_step_handler(message, get_name_to, g)
def get_name_to(message, g):
    g.date_to = message.text
    currencies.get_graphs(g.y, g.x, g.date_from, g.date_to)
    bot.send_photo(message.chat.id, open('graph.png', 'rb'))

    
def listener(messages):
    for mes in messages:
        continue

bot.set_update_listener(listener)

bot.polling(none_stop=True, interval=0)
