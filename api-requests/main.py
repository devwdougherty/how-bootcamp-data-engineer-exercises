import requests
import json
import backoff
import random
import logging

# Configuring logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

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
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    random_n = random.random()
    #print(f"""
    #        RND: {random_n}
    #        args: {args if args else 'no args'}
    #        kwargs: {kargs if kargs else 'no kwargs'}
    #""")
    log.debug(f"RND: {random_n}")
    log.info(f"args: {args if args else 'no args'}")
    log.info(f"kwargs: {kargs if kargs else 'no kwargs'}")

    if random_n < .2:
        log.error('Connection was finalized')
        raise ConnectionAbortedError('Connection was finalized')
    elif random_n < .4:
        log.error('Connection was denied')
        raise ConnectionRefusedError('Connection was denied')
    elif random_n < .6:
        log.error('Awaiting time exceed')
        raise TimeoutError('Awaiting time exceed')
    else:
        return "OK!"

test_func()
test_func(52)
test_func(42, 51, name='will')