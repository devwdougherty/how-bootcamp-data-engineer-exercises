import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

# Configuring logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

url = 'https://portalcafebrasil.com.br/todos/podcasts/'

ret = requests.get(url)

ret.text

soup = bs(ret.text)

soup.find('h5')
soup.find('h5').text
soup.find('h5').a['href']

item_list_podcast = soup.find_all('h5')

for item in item_list_podcast:
    print(f"EP: {item.text} - Link: {item.a['href']}")

"""
    Through Chrome dev tools (Network tab) we discovered that portalcafebrasil website loads more and more podcasts links
    when we keep scrolling the page, and that 'ajax=true' is responsible for that.

    'ajax=true' it's a piece of the webpage that contain a lot less htlm elements than the entire page and have our target tags:
    podcast title (h5 - text) and link (a - href)

    20/10/2022: Each page seems to load 16 items per time. (Total at this date: 844 episodes)

    'https://portalcafebrasil.com.br/todos/podcasts/page/1/?ajax=true' -> Latest podcasts episodes
    'https://portalcafebrasil.com.br/todos/podcasts/page/2/?ajax=true'
"""
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

def get_podcast_page_items(page):
    ret = requests.get(url.format(page))
    soup = bs(ret.text)
    return soup.find_all('h5')

index = 1
podcast_list = []
items_got_list = get_podcast_page_items(index)
log.debug(f"Collected {len(items_got_list)} episodes from link: {url.format(index)}")
"""
    We discovered that when we got an inexistent page number (exceeding the number of existent episodes - considering 16 per page)
    soup will return nothing (0) for us.
"""
while len(items_got_list) > 0:
    podcast_list = podcast_list + item_list_podcast
    index += 1
    items_got_list = get_podcast_page_items(index)
    log.debug(f"Collected {len(items_got_list)} episodes from link: {url.format(index)}")

print(len(podcast_list))
print(podcast_list)

df = pd.DataFrame(columns=['name', 'link'])

for item in podcast_list:
    df.loc[df.shape[0]] =  [item.text, item.a['href']]

print(df)

# index -> generate a first column not present in the original dataframe. Could result in parsing error using Excel.
df.to_csv('podcast_database.csv', sep=';', index=False)