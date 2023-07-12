import telebot
import requests
import random

from telebot import types
from googletrans import Translator

# utils

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')
translator = Translator()
weather_api_key = 'abc243dccda528959fc3d2dd6f8ab61a'
meme_api_url = "https://programming-memes-images.p.rapidapi.com/v1/memes?rapidapi-key" \
               "=1db773f93dmsh3e0725f197b19f6p19106bjsn5b1f8177ea85"

# global var's

language = None
city = None
state = None
text = None

# keyboard button sets

lang_keyboard = types.ReplyKeyboardMarkup()
ru_lang = types.KeyboardButton('🇷🇺Русский')
en_lang = types.KeyboardButton('🇬🇧English')
lang_keyboard.add(ru_lang, en_lang)

menu_keyboard_ru = types.ReplyKeyboardMarkup(row_width=2)
trans_ru = types.KeyboardButton('🌐 Переводчик')
calc_ru = types.KeyboardButton('🧮 Калькулятор')
weather_ru = types.KeyboardButton('🌡️ Погода')
meme_ru = types.KeyboardButton('🗿 IT мем дня')
settings_ru = types.KeyboardButton('🔙 Вернуться к выбору языка')
menu_keyboard_ru.add(trans_ru, calc_ru, weather_ru, meme_ru, settings_ru)

menu_keyboard_en = types.ReplyKeyboardMarkup(row_width=2)
translator_en = types.KeyboardButton('🌐 Translator')
calc_en = types.KeyboardButton('🧮 Calculator')
weather_en = types.KeyboardButton('🌡️ Weather')
meme_en = types.KeyboardButton('🗿 IT-meme of the day')
settings_en = types.KeyboardButton('🔙 Get back to language select')
menu_keyboard_en.add(translator_en, calc_en, weather_en, meme_en, settings_en)

in_keyboard_ru = types.ReplyKeyboardMarkup(row_width=2)
back_to_menu_ru = types.KeyboardButton('🔙 Вернуться в меню')
in_keyboard_ru.add(back_to_menu_ru)

in_keyboard_en = types.ReplyKeyboardMarkup(row_width=2)
back_to_menu_en = types.KeyboardButton('🔙 Get back to menu')
in_keyboard_en.add(back_to_menu_en)


# language select after /start cmd
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, '✋😃Выберите язык / Choose language:', reply_markup=lang_keyboard)


# bot main
@bot.message_handler(content_types=['text'])
def main(message):

    global language, city, state, text
    # language selection
    if message.text == '🇷🇺Русский':
        state = 'ru_menu'
        language = 'ru'
        bot.send_message(message.chat.id, 'Выберите функцию: ', reply_markup=menu_keyboard_ru)
        state = None
    elif message.text == '🇬🇧English':
        state = 'en_menu'
        language = 'en'
        bot.send_message(message.chat.id, 'Choose function: ', reply_markup=menu_keyboard_en)
        state = None

    # it meme of the day

    elif '🗿' in message.text:
        state = 'meme'
        try:
            response = requests.get(meme_api_url).json()
            if response and isinstance(response, list) and len(response) > 0:
                images = [mem.get("image") for mem in response]
                random_image = random.choice(images)
                bot.send_photo(message.chat.id, random_image)
            elif language == 'ru':
                bot.send_message(message.chat.id, 'Не удалось получить IT-мем дня.')
            elif language == 'en':
                bot.send_message(message.chat.id, "Couldn't get It meme of the day.")
        except Exception as e:
            bot.send_message(message.chat.id, f'Error: {str(e)}')
        state = None

    # choosing a city

    elif '🌡️' in message.text:
        state = 'weather'
        if language == 'en':
            bot.send_message(message.chat.id, '🏙️ Select a city :', reply_markup=in_keyboard_en)

        elif language == 'ru':
            bot.send_message(message.chat.id, '🏙️ Выберите город :', reply_markup=in_keyboard_ru)

    # weather conditions

    elif state == 'weather' and type(message.text) is str:
        city = message.text
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
            response = requests.get(url).json()
            if response['cod'] == 200:
                weather_data = response['weather'][0]
                conditions = weather_data['main']
                conditions_ru = translator.translate(conditions, dest='ru')
                description = weather_data['description']
                description_ru = translator.translate(description, dest='ru')
                temperature = response['main']['temp']
                humidity = response['main']['humidity']
                wind_speed = response['wind']['speed']
                if language == 'ru':
                    bot.send_message(message.chat.id, f'Погода в городе {city}:\n'
                                                      f'Основные условия: {conditions_ru.text}\n'
                                                      f'Описание: {description_ru.text}\n'
                                                      f'Температура: {temperature}°C\n'
                                                      f'Влажность: {humidity}%\n'
                                                      f'Скорость ветра: {wind_speed} м/с')
                elif language == 'en':
                    bot.send_message(message.chat.id, f'Weather in {city}:\n'
                                                      f'Main conditions: {conditions}\n'
                                                      f'Description: {description}\n'
                                                      f'Temperature: {temperature}°C\n'
                                                      f'Humidity: {humidity}%\n'
                                                      f'Wind speed: {wind_speed} м/с')
            elif language == 'ru':
                bot.send_message(message.chat.id, 'Не удалось получить данные о погоде для указанного города.')
            elif language == 'en':
                bot.send_message(message.chat.id, "Couldn't get data for this city.")
        except Exception as e:
            bot.send_message(message.chat.id, f'Error: {str(e)}')
        state = None

    # entering the text

    elif '🌐' in message.text:
        state = 'trans'
        if language == 'en':
            bot.send_message(message.chat.id, '🔠 Enter the text for translation:', reply_markup=in_keyboard_en)
        elif language == 'ru':
            bot.send_message(message.chat.id, '🔠️ Введите текст для перевода :', reply_markup=in_keyboard_ru)

    # translator

    elif state == 'trans' and type(message.text) is str:
        text = message.text
        try:
            detected_lang = translator.detect(text).lang
            if detected_lang == 'ru':
                translation = translator.translate(text, dest='en')
                if language == 'en':
                    bot.send_message(message.chat.id, f'Translation to English: {translation.text}')
                elif language == 'ru':
                    bot.send_message(message.chat.id, f'Перевод на английский: {translation.text}')
            else:
                translation = translator.translate(text, dest='ru')
                if language == 'en':
                    bot.send_message(message.chat.id, f'Translation to Russian: {translation.text}')
                elif language == 'ru':
                    bot.send_message(message.chat.id, f'Перевод на русский: {translation.text}')
        except AttributeError:
            if language == 'en':
                bot.send_message(message.chat.id, "Couldn't recognize the text language. Please try again.")
            elif language == 'ru':
                bot.send_message(message.chat.id, 'Не удалось определить язык текста. Пожалуйста, попробуйте еще раз.')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error: {str(e)}')
        state = None

    # enter expression

    elif '🧮' in message.text:
        state = 'calc'
        if language == 'en':
            bot.send_message(message.chat.id, '🔢 Enter the expression :', reply_markup=in_keyboard_en)
        elif language == 'ru':
            bot.send_message(message.chat.id, '🔢 Введите выражение :', reply_markup=in_keyboard_ru)

    # calculator

    elif state == 'calc':
        expression = message.text
        try:
            result = eval(expression)
            if language == 'en':
                bot.send_message(message.chat.id, f'Result : {result}')
            elif language == 'ru':
                bot.send_message(message.chat.id, f'Результат : {result}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error : {str(e)}')


bot.polling(none_stop=True, interval=0)
