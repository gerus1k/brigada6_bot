import telebot

from telebot import types

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')

# Выбор языка при вызове /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопками выбора языка
    markup = types.InlineKeyboardMarkup()
    russian_button = types.InlineKeyboardButton('🇷🇺Русский', callback_data='ru')
    english_button = types.InlineKeyboardButton('🇬🇧English', callback_data='en')
    markup.add(russian_button, english_button)

    # Отправляем сообщение с кнопками выбора языка
    bot.send_message(message.chat.id, 'Выберите язык / Choose language:', reply_markup=markup)



bot.polling(none_stop=True, interval=0)
