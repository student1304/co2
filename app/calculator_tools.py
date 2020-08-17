#imports
import pandas as pd, numpy as np
from api_tools import get_product_info
from eua_tools import fetch_eua_price
import streamlit as st


#some values
km_equiv = 7 # 7km Fahrt für 1 kg CO2
baum_equiv = 10 # 1 baum bindet 10kg Co2 pro Jahr
eua_eur = fetch_eua_price() #25.5 # eur/t

def get_web_data_for_cart(res):
    ''' update the merged result df with data from OFF scraper'''
    quantities =[]
    images = []
    packagings = []
    cat_hierarchies = []

    #todo :::: build error checker
    for gtin in res.gtin:
        info = get_product_info(gtin)
        if info['status'] == 1:
            product = info['product']
            quantities.append(product['product_quantity'])
            images.append(product['image_front_small_url'])
            packagings.append(product['packaging_tags'])
            cat_hierarchies.append(product['categories_hierarchy'])
        else:
            quantities.apped('100')
            images.append('https://www.emoji.co.uk/files/twitter-emojis/symbols-twitter/11142-black-question-mark-ornament.png')
            packagings.append(['unknown'])
            cat_hierarchies.append(['unknown'])
    res['image']=images
    res['quantity'] = quantities
    res['packaging'] = packagings
    res['category'] = cat_hierarchies
    return res

# the main function
@st.cache(suppress_st_warning=True)
def get_result(cart, df=pd.read_pickle('./app/data/co2data.pkl')):
    '''
    input a cart DataFrame file, optional: df containing co2 data by gtin
    returns: df with calculation results for co2, km equivalent, baumjahre equivalent
    '''
    #prepare format in cart
    cart.GTIN = [np.int64(gtin) for gtin in cart.GTIN]
    cart['TOTAL'] = cart.AMOUNT * cart.PRICE
    cart['gtin'] = cart.GTIN
    cart.drop(columns='GTIN')
    # lookup co2 values from pickle db
    res = df.merge(cart, on='gtin')
    res.drop(columns='GTIN')
    res.co2 = [np.float(item) for item in res.co2]
    res = get_web_data_for_cart(res) # query api for size, packaging etc
    
    #res.co2 in kg CO2 pro unit of product
    res['kg_co2'] = res.co2/res['units(g)'] * res.quantity * res.AMOUNT # kg CO2 pro unit / units(g) = kg CO2 pro 1g -> * quant(g) = kg CO2 pro produkteinheit -> *AMOUNT = kg CO2 line
    res['eur_co2']=res.kg_co2/1000 * eua_eur # kg CO2 in t (/1000) * eur/t
    res['km_equiv'] = res.kg_co2 * km_equiv
    res['baumjahre'] = res.kg_co2 / baum_equiv
    
    mycolumns = list('NAME gtin co2 kg_co2 eur_co2 km_equiv baumjahre'.split(' '))
    return res[mycolumns]

def  get_chart_data(res):
    columns = 'kg_CO2 EUR_CO2 Auto_100km Baumjahre'.split(' ')
    values = [res.kg_co2.sum(), res.eur_co2.sum(), res.km_equiv.sum()/100, res.baumjahre.sum()]
    chart_data = pd.DataFrame(index=columns, data=values)
    return chart_data