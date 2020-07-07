import streamlit as st
import pandas as pd
#import numpy as np
#import time
from api_tools import get_product_info


# load md text from file and display on page
path_to_md = "./intro.md"
with open(path_to_md, "r") as f:
    md_text = f.read()
st.markdown(md_text)

# load and display cart
cart_csv = st.file_uploader('Drag&Drop CSV oder Upload hier', type="csv")
if cart_csv is not None:
    data = pd.read_csv(cart_csv, sep=',', decimal='.')
    st.write(data)

    #loop through cart and show categories
    for gtin in data.GTIN:
        #st.write(gtin)
        info = get_product_info(gtin)
        st.write('getting info for... ', gtin)
        if info['status'] != 1:
            st.markdown('   - **no info** available in openfoodfacts.org')
        else:
            image_url = info['product']['selected_images']['front']['thumb']['de']
            st.markdown('![Image](%s)' %image_url)
            st.write(
                info['product']['packaging_tags'], 
                info['product']['categories_hierarchy']
            )
        