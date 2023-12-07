import telebot
import os

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

# Handles '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.reply_to(message, "What do you want to do today?")

# Handles help
@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.reply_to(message, "Who owe you money?\nAdd people who owe you money")

# Add people who owe me money
# - Calculator
# Check who owes me money
# Reminder of who owe me money
# Add bot to group chat and Leave when paid

bot.infinity_polling()