import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конверитировать одинаковые валюты {base} ')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}'
                               '\n Чтобы увидеть список доступных валют введите команду: /values')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}'
                               '\n Чтобы увидеть список доступных валют введите команду: /values')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не кдалось обработать колличество {amount}'
                               '\n Колличество должно быть числовым значением')

        r = requests.get(f'https://api.exchangerate.host/convert?from={base_ticker}&to={quote_ticker}')
        total_base = json.loads(r.content)['info']['rate'] * amount
        return total_base
