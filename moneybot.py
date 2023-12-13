import telebot
from telebot import types
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

confirmation = None
current_name = None
current_money = None

# Handles '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	btn1 = types.KeyboardButton("/add")
	btn2 = types.KeyboardButton("/who")
	btn3 = types.KeyboardButton("/help")
	btn4 = types.KeyboardButton("/back")
	markup.add(btn1,btn2)
	markup.add(btn3,btn4)
	bot.send_message(chat_id=message.chat.id, text="What do you want to do today?", reply_markup=markup)

# Handles '/help'
@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.reply_to(message, "/add - Add people who owe you money\n/who - Who owe you money?")

# Handles '/add'
@bot.message_handler(commands=['add'])
def handle_add(message):
	bot.reply_to(message, "Who owes you money?")
	bot.register_next_step_handler(message, get_name)
	
# Handles '/who'
@bot.message_handler(commands=['who'])
def handle_who(message):
	bot.reply_to(message, "People owing you money")

# Handles '/back'
@bot.message_handler(commands=['back'])
def handle_back():
	pass

def get_name(message):
	current_name = message.text
	try:
		current_name = str(message.text)
		bot.reply_to(message, f"{current_name} owes you money")
		bot.reply_to(message, "How much money is owed?")
		bot.register_next_step_handler(message, get_money)
	except ValueError:
		bot.reply_to(message, "Invalid input. Please enter a valid name.")
	
	
def get_money(message):
	try:
		current_money = float(message.text)
		bot.reply_to(message, f"{current_name} owes you ${current_money}")
		bot.register_next_step_handler(message, record_money)
	except ValueError:
		bot.reply_to(message, "Invalid input. Please enter a valid amount.")

def record_money(message):
	# cursor.execute("SELECT * FROM user WHERE id=?", (current_name,))
	# if not cursor.fetchone():
	# 	cursor.execute("INSERT INTO user (id) VALUES (?)", (current_name,))
	# cursor.execute("INSERT INTO money_owed (id, money) VALUES (?, ?)", (current_name, current_money))

	# conn.commit()

	bot.reply_to(message, "Payment Recorded!")


bot.polling()