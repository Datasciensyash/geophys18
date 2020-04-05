import streamlit as st 
import numpy as np 

txt = st.text_input('Find ae', value='1,1 3,2 4,1')
arr = list(map(float, txt.replace(',', '.').replace('	', ' ').split(' ')))

st.info(f'{round(np.array(arr).prod(), 4)}')


txt = st.text_input('Find ae sum', value='1,1 3,2 4,1')
arr = list(map(float, txt.replace(',', '.').replace('	', ' ').split(' ')))

ae = np.array(arr).mean()
st.info(f'{round(ae, 5)}')
st.success(f'{round((ae * 1e-3)  / (1 - 0.5 * (ae * 1e-3)), 5) * 1000}')
