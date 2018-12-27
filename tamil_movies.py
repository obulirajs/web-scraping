from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn


url = 'https://www.imdb.com/search/title?release_date=2018-01-01,2018-12-23&languages=ta&start=51&ref_=adv_nxt'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

years = []
names = []

start_time = time()
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Preparing the monitoring of the loop
start_time = time()
requests = 0
pages = [str(i) for i in range(0,8)]
j=50
years_url = '2018'
# print(years_url)
for page in pages:
    page = str(int(page) * 50 + 1)
    print(page)
    response = get('https://www.imdb.com/search/title?release_date=2018-01-01,2018-12-31&languages=ta&start='+page, headers = headers)
    # Pause the loop
    sleep(randint(8,15))
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    if requests > 72:
        warn('Number of requests was greater than expected.')
        break
    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')
    
    my_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
    for container in my_containers:
        if container.find('div') is not None:
            name = container.h3.a.text
            names.append(name)
            year = container.h3.find('span', class_ = 'lister-item-year').text
            years.append(year)

movie_ratings = pd.DataFrame({'movie': names, 'year': years})
movie_ratings.drop_duplicates()
# print(movie_ratings)