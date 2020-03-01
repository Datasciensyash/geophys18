import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modules import get_coeffs, get_K
import pandas as pd
import cv2

A_values = st.text_input('Values of A', value='2.2, 2.05, 1.9')
A_values = np.array(eval('[' + A_values + ']')) #That is bad.

P_values = st.text_input('Values of P', value='65, 72, 75')
P_values = np.array(eval('[' + P_values + ']')) #That is bad.

H_values = st.text_input('Values of H', value='65, 72, 75')
H_values = np.array(eval('[' + H_values + ']')) #That is bad.

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
    #grid = []
    #for i in range(7):
        #for j in range(15):
            #grid.append([i, j, KM_values[i * 7 + j]])
    #print(grid)
    #pd.DataFrame(grid).to_csv(f'grid-{filename}', index=False)
    pd.DataFrame(KM_values.reshape(15, 7), index='1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'.split(' '), columns='I II III IV V VI VII'.split(' ')).to_csv(f'grid-{filename}', index=False)
    df.to_csv(filename, index=False)


try:
    plt.figure(figsize=(8, 8))
    image = cv2.resize(KM_values.reshape(7, 15).astype('float'), (3000, 3500), interpolation=cv2.INTER_CUBIC)
    for i in range(0, int(image.max() // 100) + 1):
        image = np.where((image < (100 * (i + 1))) & (image > (100 * i)), i, image)




    plt.imshow(image.astype(np.uint8))
    plt.colorbar(ticks=range(7), label='sex')
    st.pyplot()

    def discrete_matshow(data):
        #get discrete colormap
        cmap = plt.get_cmap('viridis', np.max(data)-np.min(data)+1)
        # set limits .5 outside true range
        mat = plt.matshow(data, cmap=cmap,vmin = np.min(data)-.5, vmax = np.max(data)+.5)
        #tell the colorbar to tick at integers
        cax = plt.colorbar(mat, ticks=np.arange(np.min(data), np.max(data) + 1))
        cax.ax.set_yticklabels([f'{i * 100}' for i in range(int(np.max(data)) + 1)])
        cax.ax.set_title(r'$К_{m}$ $\frac {м^2}{сут}$', fontsize=12)

    discrete_matshow(image.astype(np.uint8))

    plt.xlabel("TA")
    plt.ylabel("DA")
    st.pyplot()
except:
    st.info('Waiting for data...')