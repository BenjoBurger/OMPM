import telebot
from telebot import types
import os
import sqlite3

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
def handle_back(message):
	pass

def get_name(message):
	current_name = message.text
	bot.reply_to(message, f"{current_name} owes you money")
	bot.reply_to(message, "How much money is owed?")
	bot.register_next_step_handler(message, get_money)
	
def get_money(message):
		try:
			current_money = float(message.text)
			bot.reply_to(message, f"{current_name} owes you ${current_money}")
		except ValueError:
			bot.reply_to(message, "Invalid input. Please enter a valid amount.")

def handle_confirm(message):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton("Yes", callback_data="Yes")
	btn2 = types.InlineKeyboardButton("No", callback_data="No")
	markup.add(btn1,btn2)
	bot.send_message(message.chat.id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	if (call.data == "Yes"):
		confirmation = 1
	return


# Main Functionalities:
# Handle start and help
# - Start
# - Help: Drop down menu? / Functions inside
# Add people who owe me money
# - How to calculate: Each person / Split among people
# - Calculator: create keypad?
# - QOL: GST + SST / GST / SST
# - Splitting among people
# Check who owes me money
# Reminder of who owe me money

bot.polling()