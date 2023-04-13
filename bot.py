import time
import telebot
from ExchangeRate import ExchangeRate
class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.exchange_rate = ExchangeRate()
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['usd'])(self.usd)
        self.bot.message_handler(commands=['set_limits'])(self.set_limits)
        self.bot.polling()

    def start(self, message):
        self.bot.reply_to(
            message, 'Привет! Я бот, который будет присылать тебе курс доллара, если он выйдет за заданные границы.')

    def help(self, message):
        self.bot.reply_to(
            message, 'Для получения курса доллара отправь мне команду /usd. Для установки границ отправь мне команду /set_limits')

    def set_limits(self, message):
        self.bot.reply_to(message, 'Введите нижнюю границу курса доллара:')
        self.bot.register_next_step_handler(message, self.set_lower_limit)

    def set_lower_limit(self, message):
        try:
            self.exchange_rate.lower_limit = float(message.text)
            self.bot.reply_to(message, 'Введите верхнюю границу курса доллара:')
            self.bot.register_next_step_handler(message, self.set_upper_limit)
        except ValueError:
            self.bot.reply_to(message, 'Неверный формат числа. Попробуйте еще раз.')
            self.bot.register_next_step_handler(message, self.set_lower_limit)

    def set_upper_limit(self, message):
        try:
            self.exchange_rate.upper_limit = float(message.text)
            self.bot.reply_to(message, 'Границы курса доллара успешно установлены.')
        except ValueError:
            self.bot.reply_to(message, 'Неверный формат числа. Попробуйте еще раз.')
            self.bot.register_next_step_handler(message, self.set_upper_limit)

    def usd(self, message):
        while True:
            usd_rate = self.exchange_rate.get_usd_rate()
            if usd_rate < self.exchange_rate.lower_limit or usd_rate > self.exchange_rate.upper_limit:
                self.bot.reply_to(message,
                                  'Курс доллара сейчас %s. Внимание! Курс вышел за заданные границы (%s - %s).' %
                                  (usd_rate, self.exchange_rate.lower_limit, self.exchange_rate.upper_limit))
            else:
                self.bot.reply_to(message, f'Курс доллара сейчас {usd_rate}.')
            time.sleep(60)

    def polling(self):
        self.bot.polling()
