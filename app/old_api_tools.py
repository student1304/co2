#%%
import requests
#import asyncio
from sqlite_cache.sqlite_cache import SqliteCache
cache = SqliteCache('./cache')
# https://github.com/csotelo/python-sqlite-cache

api_base = "https://world.openfoodfacts.org/api/v0/product/"
testgtin = "4008948194016" # loop through later
api_suffix = ".json"
#api_url = api_base+gtin+api_suffix


#%% get exiobase data
# https://pymrio.readthedocs.io/en/latest/notebooks/working_with_exiobase.html




# %%
#import pymrio
#io = pymrio.load_test()
# %%
#io.calc_all()
#print(io.emissions.D_exp)

#import matplotlib.pyplot as plt
#io.emissions.plot_account('emission_type1')
#plt.show()

#%%
def get_product_info(gtin):
    product = cache.get(gtin)
    if product is None:
        api_url = api_base + str(gtin) + api_suffix
        r = requests.get(api_url)
        product = r.json()
        cache.set(gtin, product, timeout=120000.0)
        
       
    return product

# info = get_product_info(gtin)

# info = get_product_info(testgtin)
# print(info['packaging'], info['image']['de'], info['category'][-1])

# %%
