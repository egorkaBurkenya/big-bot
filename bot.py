import telebot
import json
from telebot import types

with open('./config.json', 'r') as file:
    config = json.load(file)

with open('menu.json', 'r') as file:
        menuDict = json.load(file)

bot = telebot.TeleBot(config['TOKEN'])

@bot.message_handler(commands=['start'])
def send_welcome_message(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/menu")
    item2 = types.KeyboardButton("/about")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Добро пожаловать, в бот меню\n в котором вы сможете выбрать себе еду, а мы ее вкусно приготовим', reply_markup=markup)

@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = 'Menu🎈: \n\n'
    for category in menuDict:
        item = types.KeyboardButton(category)
        markup.add(item)
        menu += f'{category}\n'
        for food in menuDict[category]:
            menu += f'   {food}: {menuDict[category][food]["цена"]}$ \n'
    bot.send_message(message.chat.id, menu, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def listener(message):
    if message.chat.type == 'private': 
        try:
            category = menuDict[message.text]
            with open('./config.json', 'r') as file:
                config = json.load(file)
            config['choseCategory'] = message.text
            with open('config.json', 'w') as file:
                json.dump(config, file)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = f'Menu {message.text}: \n'
            for food in category:
                item = types.KeyboardButton(food)
                markup.add(item)
                menu += f'   {food}: {category[food]["цена"]}$ \n'
            bot.send_message(message.chat.id, menu, reply_markup=markup)
        except KeyError:
            pass
        try:
            with open('./config.json', 'r') as file:
                config = json.load(file)
            food = menuDict[config['choseCategory']][message.text]
            img = open(food['img'], 'rb')
            bot.send_photo(message.chat.id, img)
            info = f'{message.text}:\n\nцена: {food["цена"]}$\n'
            for i in food:
                if type(food[i]) == list:
                        info += f'{i}:\n'
                        for ing in food[i]:
                           info += f'* {ing}\n' 
                else:     
                    if i != 'img' and i != 'цена': 
                        info += f'{i}: {food[i]}\n'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('/buy')
            item2 = types.KeyboardButton('/menu')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, info, reply_markup=markup)
        except KeyError:
            pass

bot.polling()