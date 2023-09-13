import telebot
bot = telebot.TeleBot('6598007736:AAEsWn1fTa3c1pvG3nvO71hBh6g4dTkfwcY')
from telebot import types
import time
import sqlite3 as sql

users = []

@bot.message_handler(commands=['start'])
def startBot(message):
    con_ad = sql.connect('admin.db')
    first_mess = "Привет, Я бот-помощник-хранитель! \n Давай начнём работу!)"
    cur_ad = con_ad.cursor()
    flag = False
    cur_ad.execute("SELECT `chat_id` FROM `backlog`")
    rows = cur_ad.fetchall()
    for row in rows:
        if row == message.chat.id:
            flag = True
            break
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if flag:
        button_create = types.KeyboardButton("Подключиться к предыдущей")
        button_connect = types.KeyboardButton("Сменить бд")
        markup.add(button_create, button_connect)
        bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
    else:
        button_create = types.KeyboardButton("Создать новую бд")
        button_connect = types.KeyboardButton("Подключиться к существующей")
        markup.add(button_create, button_connect)
        bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
    con_ad.commit()
    cur_ad.close()

@bot.message_handler(commands=['Tusa'])
def TusaBot(message):
    if not (message.chat.id in users): users.append(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton("Помощь")
    markup.add(but)
    mess = message.from_user.first_name + " Затусим?)"
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    for i in range(1, 4):
        bot.send_message(message.chat.id, "\U0001F608" * i, parse_mode='html', reply_markup=markup)
        bot.send_message(message.chat.id, "\U0001F52A" * i, reply_markup=markup)

@bot.message_handler(commands=['help'])
def helps(message):
    if not (message.chat.id in users): users.append(message.chat.id)
    answ = "У меня есть команды: \n /start \n /help \n /Tusa \n"
    answ += "Я умею отвечать на: \n Привет \n Признание в любви"
    bot.send_message(message.chat.id, answ)

@bot.message_handler(content_types=['text'])
def answer(message):
    if not (message.chat.id in users): users.append(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton("Помощь")
    markup.add(but)
    if message.text == "Привет":
        answ = "Приветсвую тебя " + message.from_user.first_name + " " + message.from_user.last_name + ". Слушаю и повинуюсь!"
        bot.send_message(message.chat.id, answ, reply_markup=markup)
    elif message.text.lower().count("я") > 0 and message.text.lower().count("тебя") > 0 and message.text.lower().count("люблю") > 0:
        answ = "И я тебя очень сильно" + "\U00002764" * 3
        bot.send_message(message.chat.id, answ, reply_markup=markup)
    elif message.text == "Помощь":
        answ = "У меня есть команды: \n /start \n /help \n /Tusa \n"
        answ += "Я умею отвечать на: \n Привет \n Признание в любви"
        bot.send_message(message.chat.id, answ, reply_markup=markup)
    elif message.text in ["Сменить бд", "Подключиться к существующей"]:
        con_ad = sql.connect('admin.db')
        cur_ad = con_ad.cursor()
        cur_ad.execute("SELECT bd FROM paswd")
        rows = cur_ad.fetchall()
        markup = types.InlineKeyboardMarkup()
        for row in rows:
            markup.add(types.InlineKeyboardButton(row, callback_data=row))
        bot.send_message(message.chat.id, "Выбери одну из предложеных БД:\n", parse_mode='html', reply_markup=markup)
    else:
        answ = "Не понял Вас?" + "\U0001F612"
        bot.send_message(message.chat.id, answ, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        con_ad = sql.connect('admin.db')
        cur_ad = con_ad.cursor()
        cur_ad.execute("SELECT bd FROM paswd")
        rows_change = cur_ad.fetchall()
        if function_call.data == "yes":
            second_mess = "Мы облачная платформа для разработчиков и бизнеса. Более детально можешь ознакомиться с нами на нашем сайте!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://timeweb.cloud/"))
            bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            bot.answer_callback_query(function_call.id)
        elif function_call.data == "no":
            second_mess = "Печально Очень :( Лови польскую корову)))"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Польская корова пляшет", url="https://www.youtube.com/watch?v=kk3_5AHEZxE"))
            bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            bot.answer_callback_query(function_call.id)
        elif function_call.data == "help":
            answ = "У меня есть команды: \n /start \n /help \n /Tusa \n"
            answ += "Я умею отвечать на: \n Привет \n Признание в любви"
            bot.send_message(function_call.message.chat.id, answ)
            bot.answer_callback_query(function_call.id)
        elif function_call.data in rows_change:
            cur_ad.execute(f"UPDATE backlog SET bd = '{function_call.data}'WHERE chat_id = '{function_call.message.chat.id}")
            con_ad.commit()
            cur_ad.execute("SELECT chat_id FROM backlog")
            rows1 = cur_ad.fetchall()
            if not (function_call.message.chat.id in rows1):
                cur_ad.execute(f"INSERT INTO backlog VALUES ('{function_call.message.chat.id, function_call.data}')")
            con_ad.commit()
            cur_ad.close()



bot.infinity_polling()