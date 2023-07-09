import telebot
import googletrans
import requests
import random

from telebot import types
from googletrans import Translator

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')
translator = Translator()
weather_api_key = 'abc243dccda528959fc3d2dd6f8ab61a'
meme_api_url = "https://programming-memes-images.p.rapidapi.com/v1/memes?rapidapi-key=1db773f93dmsh3e0725f197b19f6p19106bjsn5b1f8177ea85"

# Хранение состояний пользователя (какой функцией сейчас пользуется)
user_states = {}

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
    user_states[call.from_user.id] = 'translator'
    bot.send_message(call.message.chat.id, 'Введите текст для перевода:')

# Обработка ввода текста для перевода (НЕ РАБОТАЕТ)) )
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'translator')
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

    user_states[message.from_user.id] = None

# Обработка выбора функции калькулятора
@bot.callback_query_handler(func=lambda call: call.data == 'calculator')
def calculator_callback(call):
    user_states[call.from_user.id] = 'calculator'  # Установка состояния
    bot.send_message(call.message.chat.id, 'Введите выражение для вычисления:')

# Обработка ввода выражения для калькулятора
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'calculator')
def calculate_expression(message):
    expression = message.text
    try:
        result = eval(expression)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при вычислении выражения: {str(e)}')

    # Сброс состояния
    user_states[message.from_user.id] = None

# Обработка выбора функции погоды
@bot.callback_query_handler(func=lambda call: call.data == 'weather')
def weather_callback(call):
    user_states[call.from_user.id] = 'weather'
    bot.send_message(call.message.chat.id, 'Введите город:')

# Обработка выбранного населенного пункта и вывод погоды
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'weather')
def get_weather(message):
    city = message.text
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
        response = requests.get(url).json()
        if response['cod'] == 200:
            weather_data = response['weather'][0]
            main = weather_data['main']
            description = weather_data['description']
            temperature = response['main']['temp']
            humidity = response['main']['humidity']
            wind_speed = response['wind']['speed']
            bot.send_message(message.chat.id, f'Погода в городе {city}:\n'
                                              f'Основные условия: {main}\n'
                                              f'Описание: {description}\n'
                                              f'Температура: {temperature}°C\n'
                                              f'Влажность: {humidity}%\n'
                                              f'Скорость ветра: {wind_speed} м/с')
        else:
            bot.send_message(message.chat.id, 'Не удалось получить данные о погоде для указанного города.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')

    user_states[message.from_user.id] = None

# Обработка IT-мемчик дня
@bot.callback_query_handler(func=lambda call: call.data == 'meme')
def meme_callback(call):
    try:
        response = requests.get(meme_api_url).json()
        if response and isinstance(response, list) and len(response) > 0:
            images = [mem.get("image") for mem in response]
            random_image = random.choice(images)
            bot.send_photo(call.message.chat.id, random_image)
        else:
            bot.send_message(call.message.chat.id, 'Не удалось получить IT-мем дня.')
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {str(e)}')

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