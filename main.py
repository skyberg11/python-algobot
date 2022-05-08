import telebot
import data.tags as dt
import requests 
from telebot import types
from wikis import neerc, emaxx
from lib.struct import *
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot('5318640274:AAFpFNYsF-Xq3hpBSvUXerQUZ3yMKWHR9n0')

wikis = "\n<b>/neerc</b>\n<b>/algocode</b>\n<b>/emaxx</b>"
thebestplace = "\n<b>/stack</b>"

def example_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/neerc быстрая сортировка"))
    markup.add(types.KeyboardButton("/stack stackoverflow"))
    return markup

@bot.message_handler(commands=["start", "help"])
def start(m, res=False):    
    bot.send_message(m.chat.id, 'Привет. Этот бот сможет помочь тебе найти алгоритм или понять в чем ошибка.',parse_mode='HTML')
    bot.send_message(m.chat.id, "Доступные вики:{}".format(wikis), parse_mode='HTML')
    bot.send_message(m.chat.id, "Поиск ошибок:{}".format(thebestplace), parse_mode='HTML', reply_markup=example_keyboard())


@bot.message_handler(commands=['neerc'])
def neerc_handler(message):
    msg = message.text.lower()[7:]
    if(len(msg) == 0):
        return
    try:
        q = neerc.query_list(msg)
    except:
        bot.send_message(message.chat.id, 'Неизвестная ошибка. Пожалуйста, переформулируйте запрос.')  
        return
    algo_handler(q, message)

@bot.message_handler(commands=['emaxx'])
def emaxx_handler(message):
    msg = message.text.lower()[7:]
    if(len(msg) == 0):
        return
    try:    
        q = emaxx.query_list(msg)
    except:
        bot.send_message(message.chat.id, 'Неизвестная ошибка. Пожалуйста, переформулируйте запрос.') 
        return
    algo_handler(q, message)

@bot.message_handler(commands=['algocode'])
def emaxx_handler(message):
    bot.send_message(message.chat.id, 'AlgocodeWiki пока не доступен.') 

def algo_handler(queries, message):
    try:
        if(len(queries) == 0):
            bot.send_message(message.chat.id, 'По данному запросу ничего не найдено.')
            return
        bot.send_message(message.chat.id, "Найдено {} статья(-ей):\n".format(str(len(queries))))
        msg = ""
        for result in queries:
            for c in dt.special:
                result.name = result.name.replace(c, "\\" + c)
                result.ref = result.ref.replace(c, "\\" + c)
            msg += "[" + result.name + "](" + result.ref + ")\n"
        bot.send_message(message.chat.id,  msg, parse_mode='MarkdownV2')
        queries[0].preview = queries[0].preview.replace("[math]", "")
        queries[0].preview = queries[0].preview.replace("[/math]", "")
        try:
            bot.send_message(message.chat.id,  queries[0].preview , parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(message.chat.id, 'Неизвестная ошибка. Пожалуйста, переформулируйте запрос.')

bot.polling(none_stop=True, interval=0)