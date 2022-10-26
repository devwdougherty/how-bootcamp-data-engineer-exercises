import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.vivareal.com.br/venda/sp/sorocaba/apartamento_residencial/?pagina{}'

# Getting the number of real state ads for our filter (like: city)
ret = requests.get(url.format(1))
soup = bs(ret.text, 'html.parser')
real_state_quantity = soup.find('strong', {'class': 'results-summary__count'}).text
real_state_quantity = float(real_state_quantity.replace('.', ''))

# real_state_quantity / len(apartments) # 692 pages = total / number of cards per page

df = pd.DataFrame(
    columns=[
        'description',
        'address',
        'area',
        'rooms',
        'bathrooms',
        'spaces',
        'price',
        'condo',
        'wlink'
    ]
)
# code editor shortcuts: (alt) or (ctrl + alt) to get a multi cursor -> hold (shift) (ctrl) and move to the final of first word

index = 0

# Here we check if the quantity of real state ads it's equal the quantity present in our dataframe.
while real_state_quantity > df.shape[0]:
    index += 1
    print(f"Index value: {index} \t\t real state quantity: {df.shape[0]}")
    ret = requests.get(url.format(index))
    soup = bs(ret.text, 'html.parser')
    apartments = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
    """
    We're going to use try - except because some fields could not exists for all our records, and we need to avoid an exception
    to be thrown because of data (.text from a null value)
    """
    for apartment in apartments:
        try:
            description = apartment.find('span', {'class': 'property-card__title'}).text.strip() # strip to remove black spaces
        except:
            description = None
        try:
            address = apartment.find('span', {'class': 'property-card__address'}).text.strip()
        except:
            address = None
        try:
            area = apartment.find('span', {'class': 'property-card__detail-value'}).text.strip()
        except:
            area = None
        try:
            rooms = apartment.find('li', {'class': 'property-card__detail-room'}).span.text.strip() # .span -> will return '2', without .span will return -> '2 Quartos'. Pick the first span ocurrence
        except:
            rooms = None
        try:
            bathrooms = apartment.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()
        except:
            bathrooms = None
        try:
            spaces = apartment.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()
        except:
            spaces = None
        try:
            price = apartment.find('div', {'class': 'property-card__price'}).p.text.strip()
        except:
            price = None
        try:
            condo_price = apartment.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condo_price = None
        try:
            wlink = 'https://www.vivareal.com.br' + apartment['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            description,
            address,
            area,
            rooms,
            bathrooms,
            spaces,
            price,
            condo_price,
            wlink
        ]

    df.to_csv('real_state_database.csv', sep=';', index=False)