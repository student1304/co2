from bs4 import BeautifulSoup
import requests
from sqlite_cache.sqlite_cache import SqliteCache
import time

cache = SqliteCache('./app/data/eua_cache') # co2 is starting dir
url = "https://markets.businessinsider.com/commodities/co2-european-emission-allowances/euro"
timestamp = time.strftime("%Y-%M-%d", time.localtime())
key = "eua_"+timestamp

def get_eua_price(key):
    '''
    Scrapes EUA price from website if not stored in Cache
    Returns price of EUA in EUR/t
    '''
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        a = soup.find('span', class_="aktien-big-font")
        eua = float(a['data-jsvalue'])
        print('EUA today:', eua)
        cache.set(key, eua)
        return eua
    if r.status_code != 200:
        eua = 25.0 #update to get last available value of ask other source
        return eua

def fetch_eua_price(key='eua_'+time.strftime("%Y-%M-%d", time.localtime())):
    '''
    Returns current EUA price (EUR / t) . Checks local cache first, then requests website if not yet stored
    
    Usage: eua= return_eua_price(key)
        default key is 'eua_YYYY-MM-DD', leave emtpy for default or enter other date
    '''
    eua = cache.get(key)
    print(eua, 'in cache')
    if eua is None:
        print('requesting from website...')
        eua = get_eua_price(key)
    return eua

