import time
import telebot
from ExchangeRate import ExchangeRate
class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['usd'])(self.usd)
        self.bot.polling();

    def start(self, message):
        self.bot.reply_to(
            message, 'Привет! Я бот, который будет присылать тебе курс доллара, если он выйдет за заданные границы.')

    def help(self, message):
        self.bot.reply_to(
            message, 'Для получения курса доллара отправь мне команду /usd.')

    def usd(self, message):
        exchange_rate = ExchangeRate()
        while True:
            usd_rate = exchange_rate.get_usd_rate()
            if usd_rate < exchange_rate.lower_limit or usd_rate > exchange_rate.upper_limit:
                self.bot.reply_to(message, 'Курс доллара сейчас %s. Внимание! Курс вышел за заданные границы (%s - %s).' %
                                  (usd_rate, exchange_rate.lower_limit, exchange_rate.upper_limit))
            else:
                self.bot.reply_to(message, f'Курс доллара сейчас {usd_rate}.')
            time.sleep(60)

    def polling(self):
        self.bot.polling()
