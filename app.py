import telebot
from extension import APIException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Приступим к работе!\n \
    Чтобы произвести расчет введите текст\n \
    наименование_стартовой_валюты валюта_перевода количество\n \
    Теперь нажмите "Отправить" и узнайте курс перевода валют.\n\
    Также вы можете ввести команды: \n\
    /help - сможете прочитать подсказку\n\
    /values - узнаете какие валюты доступны\n'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком мало информации.\nВведите все по шаблону.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'При переводе {amount} единиц валюты {quote} в {base} вы получите {round(total_base, 2)} '
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
