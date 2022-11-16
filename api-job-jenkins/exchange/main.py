import requests
import json
import time

from datetime import datetime

def quote_dollar_price(real_value):
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    ret = requests.get(url)
    dollar = json.loads(ret.text)["USDBRL"]
    return(float(dollar['bid']) * real_value)

currency = quote_dollar_price(1)
time.sleep(5)
print(f"Current price: {currency}")

with open("exchange.csv", "a") as f:
    f.write(
        "{};{}\n".format(datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M'), currency)
    )