import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:'
            '\n <Валюта которую хотите конвертировать> '
            '<В какую валюту конвертировать> '
            '<Колличество конвертируемой валюты>'
            '\n'
            '\n Пример ввода: доллар рубль 1'
            '\n'
            '\n Чтобы увидеть список доступных валют введите команду: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) > 3:
            raise APIException('Слишком много параметров'
                               '\n Для ознакомления с параметрами ввода введите команду /start или /help')
        if len(value) < 3:
            raise APIException('Недостаточно параметров'
                               '\n Для ознакомления с параметрами ввода введите команду /start или /help')
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
