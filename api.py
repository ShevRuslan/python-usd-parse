import requests


class API:
    def __init__(self, params):
        self.params = params

    def get_data(self):
        response = requests.get(
            'https://www.alphavantage.co/query', params=self.params)
        return response.json()
