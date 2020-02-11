from modules import find_outliers
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

data_raw = st.text_input('Input your data', value='2.43, 2.35, 2.87, 4.57, 18.3, 2.34, 5.46')
data = np.array(eval('[' + data_raw + ']')) #That is bad.

delta = st.slider('Delta modifier', 1, 5, value=3)

lower, upper = find_outliers(data, delta)

plt.scatter([i for i in range(len(data))], data, c='b', label="Measurements")
plt.axhline(upper, c='r', label=f'Upper thresold: {round(upper, 4)}')
plt.axhline(lower, c='g', label=f'Lower thresold: {round(lower, 4)}')
plt.xlabel("N of measurement")
plt.ylabel("Measured weight")
plt.legend()

st.pyplot()