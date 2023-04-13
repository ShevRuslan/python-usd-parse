from api import API


class ExchangeRate:
    def __init__(self):
        self.api = API({
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': 'USD',
            'to_currency': 'RUB',
            'apikey': '6RGTEGBX0V56TPM1'
        })
        self.lower_limit = 60
        self.upper_limit = 70

    def get_usd_rate(self):
        data = self.api.get_data()
        usd_rate = float(
            data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        return usd_rate
