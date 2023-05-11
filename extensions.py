import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote.lower() == base.lower():
            raise ConvertionException(f'Невозможно перевести одинаковые валюты "{base.lower()}".')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{quote}".\nСписок доступных валют - команда /values')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}".\nСписок доступных валют - команда /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество "{amount}"')

        if amount <= 0:
             raise ValueError(f'Количество переводимой валюты не может быть отрицательным числом')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base.lower()]]

        return round(total_base * amount, 2)