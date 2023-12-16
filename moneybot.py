import telebot
from telebot import types
from dotenv import load_dotenv
import os
import sqlite3
import random

load_dotenv()

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

current_borrower = None
current_ahlong = None
current_money = None
current_title = None
new_id = None

# Handles '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	btn1 = types.KeyboardButton("/add")
	btn2 = types.KeyboardButton("/who")
	btn3 = types.KeyboardButton("/paid")
	btn4 = types.KeyboardButton("/help")
	btn5 = types.KeyboardButton("/back")
	markup.add(btn1,btn2,btn3)
	markup.add(btn4,btn5)
	bot.send_message(chat_id=message.chat.id, text="What do you want to do today?", reply_markup=markup)

# Handles '/help'
@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.reply_to(message, "/add - Add people who owe you money\n/who - Who owe you money?\n/paid - Remove people who paid you")

# Handles '/add'
@bot.message_handler(commands=['add'])
def handle_add(message):
	bot.send_message(message.chat.id, "Who owes you money?")
	bot.register_next_step_handler(message, get_borrower)
	
# Handles '/who'
@bot.message_handler(commands=['who'])
def handle_who(message):
	bot.send_message(message.chat.id, "People owing you money:")

	conn = sqlite3.connect('database.db')
	cursor = conn.cursor()

	cursor.execute('SELECT borrower FROM money_owed')
	borrowers = cursor.fetchall()
	for borrower in borrowers:
		cursor.execute('SELECT SUM(amount) FROM money_owed WHERE borrower = ?', borrower)
		amount = cursor.fetchone()
		bot.send_message(message.chat.id, f"{borrower[0]} owes you ${amount[0]}")

	conn.close()

def in_depth_debt(message):
	pass

# Handles '/paid'
@bot.message_handler(commands=['paid'])
def handle_who(message):
	bot.send_message(message.chat.id, "Who paid you?")

# Handles '/back'
@bot.message_handler(commands=['back'])
def handle_back():
	pass

def get_name(message):
	global current_name
	try:
		current_name = str(message.text)
		bot.send_message(message.chat.id, f"{current_name} owes you money")
		# bot.send_message(message.chat.id, "How much money is owed?")
		# bot.register_next_step_handler(message, callback=get_money)
	except ValueError:
		bot.reply_to(message, "Invalid input. Please enter a valid name.")
		bot.register_next_step_handler(message, get_name)
	
def get_borrower(message):
    global current_borrower
    current_borrower = message.text

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM borrowers WHERE username = ?', (current_borrower,))
    existing_user = cursor.fetchone()

    if existing_user:
        bot.send_message(message.chat.id, f"{existing_user[0]} still owes you money!")
    else:
        cursor.execute('INSERT INTO borrowers (username) VALUES (?)', (current_borrower,))
        conn.commit()
        bot.send_message(message.chat.id, f"{current_borrower}'s name has been saved.")

    conn.close()
    bot.send_message(message.chat.id, f"How much {current_borrower} owe you?")
    bot.register_next_step_handler(message, callback=get_money)

def get_money(message):
	global current_money

	try:
		current_money = float(message.text)
		bot.send_message(message.chat.id, f"{current_borrower} owes you ${current_money}")
		bot.send_message(message.chat.id, "Name this debt")
		bot.register_next_step_handler(message, callback=get_title)
	except ValueError:
		bot.reply_to(message, "Invalid input. Please enter a valid amount.")
		bot.register_next_step_handler(message, callback=get_money)

def get_title(message):
	global current_title
	current_title = message.text
	bot.send_message(message.chat.id, "Are the details correct?")
	bot.send_message(message.chat.id, f"Title: {current_title}\nAmount Owed: {current_money}\nBorrower: {current_borrower}")
	get_confirmation(message)

def get_confirmation(message):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text="Title", callback_data='wrong title')
	btn2 = types.InlineKeyboardButton(text="Amount", callback_data='wrong amount')
	btn3 = types.InlineKeyboardButton(text="Borrower", callback_data='wrong borrower')
	btn4 = types.InlineKeyboardButton(text="All Good!", callback_data='yay')
	markup.add(btn1,btn2,btn3)
	markup.add(btn4)
	bot.send_message(chat_id=message.chat.id, text="Click to edit any values", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
	if call.data == 'wrong title':
		bot.send_message(call.message.chat.id, "Rename this debt")
		bot.register_next_step_handler(call.message, callback=get_title)
	if call.data == 'wrong amount':
		bot.send_message(call.message.chat.id, f"How much {current_borrower} owe you?")
		bot.register_next_step_handler(call.message, callback=get_money)
	if call.data == 'wrong borrower':
		bot.send_message(call.message.chat.id, "Who owes you money?")
		bot.register_next_step_handler(call.message, callback=get_borrower)
	if call.data == 'yay':
		record_money(call.message)

def record_money(message):
	user_id = message.from_user.id
	new_id = int(random.random()*10000000000)
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	cursor.execute('INSERT INTO users (id) VALUES (?)', (user_id,))
	cursor.execute('INSERT INTO money_owed (id, title, amount, ah_long, borrower) VALUES (?,?,?,?,?)', (new_id,current_title,current_money,user_id,current_borrower))
	conn.commit()
	bot.send_message(message.chat.id, "Payment Recorded!", allow_sending_without_reply=True)

	conn.close()


if __name__ == "__main__":
    bot.polling(none_stop=True)