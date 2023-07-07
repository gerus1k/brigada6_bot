import telebot

from telebot import types

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')

# Выбор языка при вызове /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    russian_button = types.InlineKeyboardButton('🇷🇺Русский', callback_data='ru')
    english_button = types.InlineKeyboardButton('🇬🇧English', callback_data='en')
    markup.add(russian_button, english_button)

    bot.send_message(message.chat.id, 'Выберите язык / Choose language:', reply_markup=markup)

# Выводим основной интерфейс бота в зависимости от выбранного языка
@bot.callback_query_handler(func=lambda call: True)
def button(call):
    language = call.data

    if language == 'ru':
        markup = types.InlineKeyboardMarkup()
        translator_button = types.InlineKeyboardButton('Переводчик', callback_data='translator')
        calculator_button = types.InlineKeyboardButton('Калькулятор', callback_data='calculator')
        weather_button = types.InlineKeyboardButton('Погода', callback_data='weather')
        meme_button = types.InlineKeyboardButton('Мем дня', callback_data='meme')
        markup.add(translator_button, calculator_button, weather_button, meme_button)

        bot.send_message(call.message.chat.id, 'Выберите функцию:', reply_markup=markup)
    elif language == 'en':
        markup = types.InlineKeyboardMarkup()
        translator_button = types.InlineKeyboardButton('Translator', callback_data='translator')
        calculator_button = types.InlineKeyboardButton('Calculator', callback_data='calculator')
        weather_button = types.InlineKeyboardButton('Weather', callback_data='weather')
        meme_button = types.InlineKeyboardButton('Meme', callback_data='meme')
        markup.add(translator_button, calculator_button, weather_button, meme_button)

        bot.send_message(call.message.chat.id, 'Select function:', reply_markup=markup)

    bot.answer_callback_query(call.id)




bot.polling(none_stop=True, interval=0)
