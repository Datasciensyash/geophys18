from modules import find_outliers
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

data_raw = st.text_input('Input your data', value='2.43, 2.35, 2.87, 4.57, 18.3, 2.34, 5.46')
data = np.array(eval('[' + data_raw + ']')) #That is bad.

delta = st.slider('Delta modifier', 1, 5, value=3)

lower, upper, distribution, etc, ro_average, delta_sigma = find_outliers(data, delta)

colors = ['g' if i else 'r' for i in (data > (lower - 1e-6)) & (data < (upper + 1e-6))]

x = [i for i in range(len(distribution))]
plt.bar(x, distribution)
plt.xticks(x, [f'{round(etc[3] + etc[2] * i, 1)} - {round(etc[3] + etc[2] * (i + 1), 1)}' for i in x], rotation=20, size=7)
plt.xlabel("density")
plt.ylabel("Number of measurements")
st.pyplot()
plt.cla()

plt.scatter([i for i in range(len(data))], data, c=colors, label="Measurements")
plt.axhline(upper, c='r', label=f'Upper threshold: {round(upper, 4)}')
plt.axhline(lower, c='g', label=f'Lower threshold: {round(lower, 4)}')

plt.axhline(ro_average - delta_sigma, c='c', label=f'Upper predicted density {round(ro_average - delta_sigma, 3)}', alpha=0.15)
plt.axhline(ro_average, c='c', label=f'Avg. predicted density {round(ro_average, 3)}', alpha=0.5)
plt.axhline(ro_average + delta_sigma, c='c', label=f'Upper predicted density {round(ro_average + delta_sigma, 3)}', alpha=0.15)

plt.xlabel("N of measurement")
plt.ylabel("Measured density")
plt.legend(fontsize='x-small')
st.pyplot()

st.info(f'Predicted density (1) ± (4) = (6): {round(ro_average, 3)} ± {round(delta_sigma, 3)}')
st.info(f'Delta sigma (4): {round(delta_sigma, 3)}')
st.info(f'Accuracy (5): {round(etc[4], 3)}%')
st.info(f'Ro_average (3): {round(etc[5], 3)}')
st.info(f'Sigma average: {round(etc[0], 3)}')
st.info(f'Delta-value (2): {round(etc[1], 3)}')

st.subheader('Statistics for true measurements.')
st.success(f'Max density: {np.max(data[(data > (lower - 1e-6)) & (data < (upper + 1e-6))])}, Min density: {np.min(data[(data > (lower - 1e-6)) & (data < (upper + 1e-6))])}')
st.success(f'Mean density: {round(data[(data > (lower - 1e-6)) & (data < (upper + 1e-6))].mean(), 2)} ± {round(data[(data > (lower - 1e-6)) & (data < (upper + 1e-6))].std(), 2)}')

st.subheader('Statistics for all measurements.')
st.info(f'Max density: {np.max(data)}, Min density: {np.min(data)}')
st.info(f'Mean density: {round(data.mean(), 2)} ± {round(data.std(), 2)}')