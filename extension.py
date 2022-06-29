import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()
        
        if quote == base:
            APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ввели неверную валюту\n Попробуйте снова, но не сломайте бота!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ввели неверную валюту\n Попробуйте снова, но не сломайте бота!')

        try:
            amount = float(amount)
            if amount <= 0:
                amount = abs(amount)

        except ValueError:
            raise (f'Не удалось обработать количество {amount}')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
