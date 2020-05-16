from modules import find_outliers
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

data_raw = st.text_input('15, 15, 16, 19, 70, 55, 30, 20, 16, 16, 18, 20, 600, 40, 100, 25, 38, 18, 15, 17, 29')
data = np.array(eval('[' + data_raw + ']')) #That is bad.

delta = st.slider('Delta modifier', 1, 5, value=3)

lower, upper, distribution, etc, ro_average, delta_sigma = find_outliers(data, delta)

colors = ['g' if i else 'r' for i in (data > (lower - 1e-6)) & (data < (upper + 1e-6))]

x = [i for i in range(len(distribution))]
plt.bar(x, distribution)
plt.xticks(x, [f'{round(etc[3] + etc[2] * i, 1)} - {round(etc[3] + etc[2] * (i + 1), 1)}' for i in x], rotation=16, size=7)
plt.xlabel("Интенсивность гамма-измерения, Iγ")
plt.ylabel("Количество измерений, N")
st.pyplot()
plt.cla()

plt.scatter([i for i in range(len(data))], data, c=colors, label="Измерения")
plt.axhline(upper, c='r', label=f'Iγ_min (аномальная): {round(upper, 4)}')

plt.xlabel("Номер измерения, n")
plt.ylabel("Интенсивность гамма-излучения, Iγ")
plt.legend(fontsize='x-small')
st.pyplot()
