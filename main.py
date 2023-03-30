import requests
import telebot
import time

# задаем границы курса доллара
lower_limit = 60
upper_limit = 70

# задаем параметры запроса к API
params = {
    'function': 'CURRENCY_EXCHANGE_RATE',
    'from_currency': 'USD',
    'to_currency': 'RUB',
    'apikey': '6RGTEGBX0V56TPM1'
}

# создаем Telegram-бота
bot = telebot.TeleBot('6281992521:AAEtYZUqrpz2S53KJ0GR6i7k-YHvGJSyIgg')

# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот, который будет присылать тебе курс доллара, если он выйдет за заданные границы.')

# обрабатываем команду /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Для получения курса доллара отправь мне команду /usd.')

# обрабатываем команду /usd
@bot.message_handler(commands=['usd'])
def send_usd_rate(message):
    while True:
        # отправляем запрос к API
        response = requests.get('https://www.alphavantage.co/query', params=params)
        data = response.json()

        # получаем текущий курс доллара
        usd_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

        if usd_rate < lower_limit or usd_rate > upper_limit:
            bot.reply_to(message, f'Курс доллара сейчас {usd_rate}. Внимание! Курс вышел за заданные границы ({lower_limit} - {upper_limit}).')
        else:
            bot.reply_to(message, f'Курс доллара сейчас {usd_rate}.')

        # ждем 1 минуту перед следующим запросом
        time.sleep(60)

# запускаем бота
bot.polling()