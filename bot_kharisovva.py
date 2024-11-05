import telebot
from config import TOKEN, keys
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


# отправка сообщений на команды start / help
@bot.message_handler(commands=['start', 'help'])
def start_and_help(message: telebot.types.Message):
    text = ('Чтобы конвертировать валюту, введите команду боту в следюущем формате: \
\n<название валюты, которую хотите перевести> \
<название валюты, в которую вы хотите перевести первую валюту> \
<количество переводимой валюты> \
\n\n Увидеть список всех доступных для конвертации валют: /values')
    bot.send_message(message.chat.id, text)


# отправка сообщения по команде values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# конвертация валюты
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверный формат запроса, введите еще раз')

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду, попробуйте еще раз позднее\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)