import telebot
from telebot import types
import os

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

# Handles '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	btn1 = types.KeyboardButton("/add")
	btn2 = types.KeyboardButton("/who")
	btn3 = types.KeyboardButton("/help")
	markup.add(btn1,btn2)
	markup.add(btn3)
	bot.send_message(chat_id=message.chat.id, text="What do you want to do today?", reply_markup=markup)

# Handles help
@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.reply_to(message, "/add - Add people who owe you money \n/who - Who owe you money?")

@bot.message_handler(commands=['add'])
def handle_add(message):
	bot.reply_to(message, "Who owe you money")

@bot.message_handler(commands=['who'])
def handle_who(message):
	bot.reply_to(message, "Who owing you money")

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