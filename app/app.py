import streamlit as st
import pandas as pd
from PIL import Image
#import numpy as np
#import time
# from api_tools import get_product_info
#from eua_tools import fetch_eua_price
from calculator_tools import get_result, get_chart_data
from streamlit_tools import download_link


# load md text from file and display on page
image = Image.open("./app/co2bon-logo.png")
st.image(image, format='png')
path_to_md = "./app/intro.md" # seen from co2 folder
with open(path_to_md, "r") as f:
    md_text = f.read()
st.markdown(md_text)

# get current co2 price and display
#eua = fetch_eua_price()
#st.write('EUA Price today is:', eua, 'EUR/t CO2')



# load and display cart
cart_csv = st.file_uploader('Drag&Drop CSV oder Upload hier', type="csv")

# button to use pre-defined csv
if st.button('Hier klicken um Beispiel-Warenkorb 1 zu verwenden'):
    cart_csv = './app/cart1.csv'

if st.button('Hier klicken um Beispiel-Warenkorb 2 zu verwenden'):
    cart_csv = './app/cart2.csv'

if cart_csv is not None:
    cart = pd.read_csv(cart_csv, sep=',', decimal='.')
    st.write('Danke! Ich habe folgende Information erhalten:', cart)
    progbar = st.progress(0)

    res = get_result(cart)
    st.write('Ergebnisse der Rechnung: ', res)
    
    chart_data = get_chart_data(res)
    progbar.progress(50)

    #download button
    #if st.button('Download der Ergebnisse erzeugen'):
    tmp_download_link = download_link(res, 'results.csv', 'Download der Ergebnisse als .csv')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    #bar chart
    st.bar_chart(chart_data)
    progbar.progress(75)

    #Ergbnisse als Text
    st.markdown('# CO2 für diesen Einkauf:')
    st.write(f'CO2: **{res.kg_co2.sum():.2f} kg**')
    st.write(f'Das entspricht: **{res.baumjahre.sum():.2f} Baumjahren**')
    st.write(f'In Autokilometern: **{res.km_equiv.sum():.2f} km Fahrstrecke**')
    st.write(f'In EURO: \t\t **{res.eur_co2.sum():.2f} EUR**')
    progbar.progress(100)


        