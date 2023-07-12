import telebot
import requests
import random

from telebot import types
from googletrans import Translator

bot = telebot.TeleBot('6022109518:AAHgixLTjERH8Caogmg_lsz1v2y5D38iNIg')
translator = Translator()
weather_api_key = 'abc243dccda528959fc3d2dd6f8ab61a'
meme_api_url = "https://programming-memes-images.p.rapidapi.com/v1/memes?rapidapi-key=1db773f93dmsh3e0725f197b19f6p19106bjsn5b1f8177ea85"

language = None
city = None
state = None
text = None


# language select after /start cmd
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('🇷🇺Русский')
    btn2 = types.KeyboardButton('🇬🇧English')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, 'Выберите язык / Choose language:', reply_markup=markup)


# bot main
@bot.message_handler(content_types=['text'])
def main(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    global language, city, state, text
    # language selection
    if message.text == '🇷🇺Русский':
        state = 'ru_menu'
        language = 'ru'

        btn1 = types.KeyboardButton('🌐 Переводчик')
        btn2 = types.KeyboardButton('🧮 Калькулятор')
        btn3 = types.KeyboardButton('🌡️ Погода')
        btn4 = types.KeyboardButton('🗿 IT мем дня')
        btn5 = types.KeyboardButton('🔙 Вернуться к выбору языка')
        markup.add(btn1, btn2, btn3, btn4, btn5)

        bot.send_message(message.chat.id, '<pre>    Выберите функцию:</pre>', parse_mode='html', reply_markup=markup)
        state = None
    elif message.text == '🇬🇧English':
        state = 'en_menu'
        language = 'en'

        translator_button = types.KeyboardButton('🌐 Translator')
        calculator_button = types.KeyboardButton('🧮 Calculator')
        weather_button = types.KeyboardButton('🌡️ Weather')
        meme_button = types.KeyboardButton('🗿 IT-meme of the day')
        lang_select_button = types.KeyboardButton('🔙 Get back to language select')
        markup.add(translator_button, calculator_button, weather_button, meme_button, lang_select_button)

        bot.send_message(message.chat.id, '<pre>    Choose function:</pre>', parse_mode='html', reply_markup=markup)
        state = None
    elif '🗿' in message.text:
        state = 'meme'
        try:
            response = requests.get(meme_api_url).json()
            if response and isinstance(response, list) and len(response) > 0:
                images = [mem.get("image") for mem in response]
                random_image = random.choice(images)
                bot.send_photo(message.chat.id, random_image)
            elif language == 'ru':
                bot.send_message(message.chat.id, 'Не удалось получить IT-мем дня :(.')
            elif language == 'en':
                bot.send_message(message.chat.id, "Couldn't get It mem of the day :(.")
        except Exception as e:
            bot.send_message(message.chat.id, f'Error: {str(e)}')
        state = None
    elif '🌡️' in message.text:
        state = 'weather'
        bot.send_message(message.chat.id, 'Select city')
    elif state == 'weather' and type(message.text) is str:
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
            bot.send_message(message.chat.id, f'Error: {str(e)}')
        state = None
    elif '🌐' in message.text:
        state = 'trans'
        bot.send_message(message.chat.id, 'Enter the text :')
    elif state == 'trans' and type(message.text) is str:
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
        state = None
    elif '🧮' in message.text:
        state = 'calc'
        bot.send_message(message.chat.id, 'Введите выражение для вычисления:')
    elif state == 'calc':
        expression = message.text
        try:
            result = eval(expression)
            bot.send_message(message.chat.id, f'Результат: {result}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка при вычислении выражения: {str(e)}')


bot.polling(none_stop=True, interval=0)
