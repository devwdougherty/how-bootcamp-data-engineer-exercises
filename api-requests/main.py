import requests
import json
import backoff
import random

# https://docs.awesomeapi.com.br/
url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
ret = requests.get(url)

# if ret -> identifies automatically if the return is good.
if ret:
    print(ret)
else:
    print('request error')

json.loads(ret.text)

def quotation(value, currency):
    url = f"https://economia.awesomeapi.com.br/json/last/{currency}"
    ret = requests.get(url)
    currency_price = json.loads(ret.text)[currency.replace('-','')]
    print(f"{value} {currency:3} costs today: {float(currency_price['bid']) * 20} {currency[-3:]}")

quotation(20, 'USD-BRL')
quotation(20, 'JPY-BRL')

try:
    quotation(20, 'USD-BRL')
except Exception as e:
    # pass
    print(e)
else:
    print("request ok")

def error_check(func): #a decorator
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} has failed.")
    return inner_func

@error_check
def quotation(value, currency):
    url = f"https://economia.awesomeapi.com.br/json/last/{currency}"
    ret = requests.get(url)
    currency_price = json.loads(ret.text)[currency.replace('-','')]
    print(f"{value} {currency:3} costs today: {float(currency_price['bid']) * 20} {currency[-3:]}")

currency_list = [
    "USD-BRL",
    "EUR-BRL",
    "BTC-BRL",
    "RPL-BRL", # inexistent
    "JPY-BRL",
]

for currency in currency_list:
    try:
        quotation(20, currency)
    except:
        #pass
        print(f"{currency} failed")

# Example to explain args and kwargs in Python functions + using backoff package to handle error and retries
# max_time and max_tries
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=2)
def test_func(*args, **kargs):
    random_n = random.random()
    print(f"""
    RND: {random_n}
              args: {args if args else 'no args'}
                   kwargs: {kargs if kargs else 'no kwargs'}
    """)
    if random_n < .2:
        raise ConnectionAbortedError('Connection was finalized')
    elif random_n < .4:
        raise ConnectionRefusedError('Connection was denied')
    elif random_n < .6:
        raise TimeoutError('Awaiting time exceed')
    else:
        return "OK!"

test_func()
test_func(52)
test_func(42, 51, name='will')