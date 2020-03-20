import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modules import get_coeffs, get_K, arr_wa
import pandas as pd
import cv2

A_values = st.text_input('Values of A', value='2.2, 2.05, 1.9')
A_values = np.array(eval('[' + A_values.replace(' ', ',') + ']')) #That is bad.

P_values = st.text_input('Values of P', value='65, 72, 75')
P_values = np.array(eval('[' + P_values.replace(' ', ',') + ']')) #That is bad.

H_values = st.text_input('Values of H', value='65, 72, 75')
H_values = np.array(eval('[' + H_values.replace(' ', ',') + ']')) #That is bad.

K_values = []
for i in range(len(A_values)):
    K_values.append(get_K(A_values[i], *get_coeffs(P_values[i])))
K_values = np.array(K_values)

KM_values = []
for i in range(len(K_values)):
    KM_values.append(K_values[i] * H_values[i])
KM_values = np.array(KM_values)

df = pd.DataFrame(list(zip(A_values, P_values, H_values, K_values, KM_values)), columns=['A', 'P', 'H', 'Kф', 'Km'])
st.table(df)
filename = st.text_input('Csv filename', value='output.csv')
if st.button('Save'):
    pd.DataFrame(KM_values.reshape(15, 7), index='1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'.split(' '), columns='I II III IV V VI VII'.split(' ')).to_csv(f'grid-{filename}', index=False)
    df.to_csv(filename, index=False)


try:
    plt.figure(figsize=(8, 8))
    arr = KM_values.reshape(7, 15).astype('float').T
    n = st.slider('n', min_value=1, max_value=25, value=1)
    det = st.slider('Denominator', min_value=0.1, max_value=1.0, value=0.1)
    arr1 = cv2.resize(arr, (4 , 8), interpolation=cv2.INTER_CUBIC).astype(np.float64)
    arr2 = cv2.resize(arr, (4 , 6), interpolation=cv2.INTER_CUBIC).astype(np.float64)
    #Priors_start
    arr1[0:7, 3] = arr1[0:7, 3] * det
    arr1[7, 0:3] = arr1[7, 0:3] * det

    arr2[0:5, 3] = arr2[0:5, 3] * det
    arr2[5, 0:3] = arr2[5, 0:3] * det

    arr1[7, 3] = arr1[7, 3] * det
    arr2[5, 3] = arr2[5, 3] * det   

    #Priors_end        
    arr1 = cv2.resize(arr1, (7 * 2 * n , 15 * n), interpolation=cv2.INTER_CUBIC)
    arr2 = cv2.resize(arr2, (7 * 2 * n , 15 * n), interpolation=cv2.INTER_CUBIC)   
    arr = (arr1 + arr2) / 2

    image = arr
    for i in range(int(image.min() // 100), int(image.max() // 100) + 1):
        image = np.where((image < (100 * (i + 1))) & (image > (100* i)), i, image)

    def discrete_matshow(data, n):
        fig, ax = plt.subplots(figsize=(8, 8))
        #get discrete colormap
        cmap = plt.get_cmap('viridis', np.max(data)-np.min(data)+1)
        # set limits .5 outside true range
        mat = ax.matshow(data, cmap=cmap, vmin = np.min(data) - 0.5, vmax = np.max(data) + 0.5)
        #tell the colorbar to tick at integers
        cax = plt.colorbar(mat, ticks=np.arange(np.min(data), np.max(data) + 1))
        cax.ax.set_yticklabels([f'{i * 100}-{(i + 1) * 100}' for i in range(int(np.max(data)) + 1)])
        cax.ax.set_title(r'$К_{m}$ $\frac {м^2}{сут}$', fontsize=25)

        picket_size = n
        profile_size = n * 2
        plt.yticks([picket_size * i for i in range(0, 15)], [i + 1 for i in range(0, 15)], rotation=0, size=7)
        plt.xticks([profile_size * i for i in range(0, 7)], [i + 1 for i in range(0, 7)], rotation=0, size=7)
        ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
        plt.xlabel("Номер профиля")
        plt.ylabel("Номер пикета")



    discrete_matshow(image.astype(np.float32), n)

    st.pyplot()
except Exception as e:
    st.info('Waiting for data...')
    st.info(str(e))