import requests
import json
from config import keys

class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        #если пользователь ввел одинаковые валюты
        if base == quote:
            raise APIException('Невозможно конвертировать одинаковые валюты')

        #если пользователь ввел недоступную валюту
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        # если пользователь ввел недоступную валюту
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        #если пользователь ввел недопустимое количество
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Не удалось обработать количество')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        required_amount = total_base * amount

        return required_amount