import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для перевода одной валюты в другую, пожалуйста, введите команду боту в следующем формате: \n <имя начальной валюты> \
<имя конечной валюты> <количество начальной валюты>.\n Пример ввода: доллар рубль 10\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n '.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
      values = message.text.split() # в скринкасте разделителем элементов списка значился один пробел, я убрала разделитель, иначе два и более пробела между параметрами приводили к ошибке

      if len(values) > 3:
        raise ConvertionException('Неверное количество параметров.')

      if len(values) < 3:
        raise ConvertionException('Неверное количество параметров либо Вы ввели параметры без пробелов.')

      quote, base, amount = values
      total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'{amount} {keys.get(quote.lower())} = {total_base} {keys.get(base.lower())}'
        bot.send_message(message.chat.id, text)

bot.polling()
