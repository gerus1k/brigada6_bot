import telebot
import googletrans

from telebot import types
from googletrans import Translator

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')
translator = Translator()

# Выбор языка при вызове /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    russian_button = types.InlineKeyboardButton('🇷🇺Русский', callback_data='ru')
    english_button = types.InlineKeyboardButton('🇬🇧English', callback_data='en')
    markup.add(russian_button, english_button)

    bot.send_message(message.chat.id, 'Выберите язык / Choose language:', reply_markup=markup)

# Обработка выбора функции переводчика
@bot.callback_query_handler(func=lambda call: call.data == 'translator')
def translator_callback(call):
    bot.send_message(call.message.chat.id, 'Введите текст для перевода:')

# Обработка ввода текста для перевода (НЕ РАБОТАЕТ)) )
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    text = message.text
    try:
        detected_lang = translator.detect(text).lang
        if detected_lang == 'ru':
            translation = translator.translate(text, dest='en')
            bot.send_message(message.chat.id, f'Перевод на английский: {translation.text}')
        else:
            translation = translator.translate(text, dest='ru')
            bot.send_message(message.chat.id, f'Перевод на русский: {translation.text}')
    except AttributeError:
        bot.send_message(message.chat.id, 'Не удалось определить язык текста. Пожалуйста, попробуйте еще раз.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')

# Выводим основной интерфейс бота в зависимости от выбранного языка
@bot.callback_query_handler(func=lambda call: True)
def button(call):
    language = call.data

    if language == 'ru':
        markup = types.InlineKeyboardMarkup(row_width=2)
        translator_button = types.InlineKeyboardButton('🌐 Переводчик', callback_data='translator')
        calculator_button = types.InlineKeyboardButton('🧮 Калькулятор', callback_data='calculator')
        weather_button = types.InlineKeyboardButton('🌡️ Погода', callback_data='weather')
        meme_button = types.InlineKeyboardButton('🗿 IT мем дня', callback_data='meme')
        lang_select_button = types.InlineKeyboardButton('🔙 Вернуться к выбору языка', callback_data='lang_select')
        markup.add(translator_button, calculator_button, weather_button, meme_button, lang_select_button)

        bot.send_message(call.message.chat.id, 'Выберите функцию:', reply_markup=markup)
    elif language == 'en':
        markup = types.InlineKeyboardMarkup(row_width=2)
        translator_button = types.InlineKeyboardButton('🌐 Translator', callback_data='translator')
        calculator_button = types.InlineKeyboardButton('🧮 Calculator', callback_data='calculator')
        weather_button = types.InlineKeyboardButton('🌡️ Weather', callback_data='weather')
        meme_button = types.InlineKeyboardButton('🗿 IT-meme of the day', callback_data='meme')
        lang_select_button = types.InlineKeyboardButton('🔙 Get back to language select', callback_data='lang_select')
        markup.add(translator_button, calculator_button, weather_button, meme_button, lang_select_button)

        bot.send_message(call.message.chat.id, 'Select function:', reply_markup=markup)

    bot.answer_callback_query(call.id)

bot.polling(none_stop=True, interval=0)