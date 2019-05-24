import json
import requests


def currencyConvert():
    currency = 'USD'
    amount = 400
    cost = 0
    centralbank = requests.get(
        'https://api.exchangeratesapi.io/latest?base=EUR', timeout=15)

    centralbankrates = json.loads(centralbank.text)
    if currency == 'EUR':
        cost = amount
    else:
        exchange = centralbankrates['rates'][currency]
        cost = int(amount/exchange)
    return centralbankrates


print(currencyConvert())
