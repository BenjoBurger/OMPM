import telebot

bot = telebot.TeleBot("6916771092:AAH8WWkj9T5RAqy_4KATGrtuP_-B7UTpKQA", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
	
bot.infinity_polling()