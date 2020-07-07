#%%
import requests
from sqlite_cache.sqlite_cache import SqliteCache
cache = SqliteCache('./cache')
# https://github.com/csotelo/python-sqlite-cache

api_base = "https://world.openfoodfacts.org/api/v0/product/"
testgtin = "4008948194016" # loop through later
api_suffix = ".json"
#api_url = api_base+gtin+api_suffix

def get_product_info(gtin):
    product = cache.get(gtin)
    if product is None:
        api_url = api_base + str(gtin) + api_suffix
        r = requests.get(api_url)
        product = r.json()
        cache.set(gtin, product, timeout=120000.0)
        
       
    return product

#  local testing 
# 
# info = get_product_info(testgtin)
# print(info['packaging'], info['image']['de'], info['category'][-1])

