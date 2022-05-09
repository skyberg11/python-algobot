import telebot
import data.tags as dt
import requests 
import data.settings
from telebot import types
from wikis import neerc, emaxx, stack
from lib.struct import *
from bs4 import BeautifulSoup as bs


bot = telebot.TeleBot(data.settings.BOT_TOKEN)

wikis = "\n<b>/neerc</b>\n<b>/emaxx</b>"
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


@bot.message_handler(commands=['neerc', 'emaxx', 'stack'])
def wiki_handler(message):
    if len(message.text.split()) == 1:
        return
    wiki, msg = message.text.lower().split(" ", 1)
    wiki = wiki[1:]
    try:
        if wiki == 'neerc':
            q = neerc.query_list(msg)
        elif wiki == 'emaxx':
            q = emaxx.query_list(msg)
        elif wiki == 'stack':
            q = stack.query_list(msg)
        else:
            bot.send_message(message.chat.id, 'Неизвестная команда.')
            return  
    except:
        bot.send_message(message.chat.id, 'Неизвестная ошибка. Пожалуйста, переформулируйте запрос.')  
        return
    queries_handler(q, message)


def queries_handler(queries, message):
    try:
        if not queries:
            bot.send_message(message.chat.id, 'По данному запросу ничего не найдено.')
            return
        bot.send_message(message.chat.id, "Найдено {} статья(-ей):\n".format(str(len(queries))))
        queries.sort(reverse=True)
        msg = ""
        index = 1
        for result in queries:
            for ch in dt.special:
                result.name = result.name.replace(ch, "\\" + ch)
                result.ref = result.ref.replace(ch, "\\" + ch)
            msg += str(index) + "\. [" + result.name + "](" + result.ref + ")" + " _Рейтинг:_ *" + str(result.priority if result.priority != 0 else "Не определен") + "*\n"
            index += 1
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