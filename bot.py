from src.config import API_TOKEN
from src.strings import WELCOME_M, RESET, UPPER, LOWER, CAPTIALIZE, REMOVE_SYM, ONE_SYMBOL, NO_FOUND

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot as tb

from colorama import Back, Fore, Style

bot = TeleBot(API_TOKEN)

markup = InlineKeyboardMarkup()

upper_button = InlineKeyboardButton(UPPER, callback_data="upper")
lower_button = InlineKeyboardButton(LOWER, callback_data="lower")
everyup_button = InlineKeyboardButton(CAPTIALIZE, callback_data="capitalize")
removesym_button = InlineKeyboardButton(REMOVE_SYM, callback_data="removesym")
#ToDo patch to txt
markup.add(upper_button, lower_button, everyup_button, removesym_button)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, WELCOME_M)

@bot.message_handler(func = lambda m: True)
def all(message):
    bot.send_message(message.chat.id, message.text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    msg = call.message
    if call.data == "upper":
        upper(msg)
    elif call.data == "lower":
        lower(msg)
    elif call.data == "capitalize":
        capitalize(msg)
    elif call.data == "removesym":
        bot.register_next_step_handler(call.message, remove_symbol, msg)
        bot.answer_callback_query(callback_query_id=call.id, text="Введите символ, который нужно исключить из текста, в чат.", show_alert=True)

def lower(msg):
    bot.edit_message_text(msg.text.lower(), msg.chat.id, msg.id, reply_markup=markup)

def upper(msg):
    bot.edit_message_text(msg.text.upper(), msg.chat.id, msg.id, reply_markup=markup)

def capitalize(msg):
    bot.edit_message_text(msg.text.capitalize(), msg.chat.id, msg.id, reply_markup=markup)

def remove_symbol(message, msg):
    if len(message.text) == 1:
        if str(message.text) in str(msg.text):
            bot.edit_message_text(msg.text.replace(str(message.text),""), msg.chat.id, msg.id, reply_markup=markup)
            bot.delete_message(msg.chat.id, message.id)
        else:
            bot.send_message(msg.chat.id, NO_FOUND)
            bot.send_message(msg.chat.id, msg.text, reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, ONE_SYMBOL)
        bot.send_message(msg.chat.id, msg.text, reply_markup=markup)

if __name__ == "__main__":
    print(f"{Fore.GREEN}[БОТ]: Бот запущен!{RESET}")
    bot.polling(none_stop=True)