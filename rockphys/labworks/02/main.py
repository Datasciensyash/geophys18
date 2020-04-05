import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modules import get_coeffs, get_K, arr_wa
import pandas as pd
import cv2

A_values = st.text_input('Values of A', value='2.2 2.05 1.9')
A_values = np.array(eval('[' + A_values.replace(',', '.').replace(' ', ',') + ']')) #That is bad.

P_values = st.text_input('Values of P', value='65 72 75')
P_values = np.array(eval('[' + P_values.replace(',', '.').replace(' ', ',') + ']')) #That is bad.

H_values = st.text_input('Values of H', value='65 72 75')
H_values = np.array(eval('[' + H_values.replace(',', '.').replace(' ', ',') + ']')) #That is bad.

K_values = []
for i in range(len(A_values)):
    K_values.append(get_K(A_values[i], *get_coeffs(P_values[i])))
K_values = np.array(K_values)

KM_values = []
for i in range(len(K_values)):
    KM_values.append(K_values[i] * H_values[i])
KM_values = np.array(KM_values)

df = pd.DataFrame(list(zip(A_values, P_values, H_values, np.around(K_values, 2), np.around(KM_values, 2))), columns=['A', 'P', 'H', 'Kf', 'Km'])
st.table(df)
filename = st.text_input('Csv filename', value='output.csv')
if st.button('Save'):
    pd.DataFrame(KM_values.reshape(15, 7), index='1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'.split(' '), columns='I II III IV V VI VII'.split(' ')).to_csv(f'grid-{filename}', index=False)
    df.to_csv(filename, index=False, sep=';')

your_map = st.checkbox('Ввести ваши KM для построения карты', value=False)
if your_map:
    KM_values = st.text_input('Values of KM', value='6,5 7,2 7,5')
    KM_values = np.array(eval('[' + KM_values.replace(',', '.').replace(' ', ',') + ']')) #That is bad.

aug_map = st.checkbox('Аугментировать карту? (Может получиться посимпатичнее)', value=False)
#make_grid = st.checkbox('Сделать сетку для ручной разрисовки?', value=False)

try:
    #ttl = st.text_input('Map title', value='Карта водопроводимости неогенового водоносного горизонта \n на основе результатов работ методом вызванной поляризации')
    plt.figure(figsize=(12, 12))
    arr = KM_values.reshape(7, 15).astype('float').T
    n = st.slider('n', min_value=1, max_value=100, value=1)
    if aug_map:
        det = st.slider('Denominator', min_value=0.0, max_value=1.0, value=0.1)
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
    else:
        arr = cv2.resize(arr, (7 * 2 * n , 15 * n), interpolation=cv2.INTER_CUBIC)

    image = arr
    for i in range(int(image.min() // 100), int(image.max() // 100) + 1):
        image = np.where((image < (100 * (i + 1))) & (image > (100* i)), i, image)

    def discrete_matshow(data, n):
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        fig, ax = plt.subplots(figsize=(8, 8))
        #get discrete colormap
        cmap = plt.get_cmap('Blues', np.max(data)-np.min(data)+1)
        # set limits .5 outside true range
        mat = ax.matshow(data, cmap=cmap, vmin = np.min(data) - 0.5, vmax = np.max(data) + 0.5)
        #tell the colorbar to tick at integers
        cax = plt.colorbar(mat, ticks=np.arange(np.min(data), np.max(data) + 1), fraction=0.032, pad=0.07)
        cax.ax.set_yticklabels([f'{i * 100}-{(i + 1) * 100}' for i in range(int(np.max(data)) + 2)])
        cax.ax.set_title(r'$К_{m}$ $\frac {м^2}{сут}$', fontsize=14)

        picket_size = n
        profile_size = n * 2

        prfl = 'I II III IV V VI VII VIII'.split(' ')
        plt.yticks([picket_size * i for i in range(0, 15)], [i + 1 for i in range(0, 15)], rotation=0, size=7)
        plt.xticks([profile_size * i for i in range(0, 7)], [prfl[i] for i in range(0, 7)], rotation=0, size=7)
        ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
        plt.xlabel("Номер профиля")
        plt.ylabel("Номер пикета")



    discrete_matshow(image.astype(np.float32), n)

    plt.grid(color='gray', linestyle='-', linewidth=0.1)
    st.pyplot()

    #if make_grid:
        #plt.cla()
        #ptslist = image
        #plt.scatter([i // 15 for i in range(7 * 2 * 15 )], [i % 15 for i in range(7 * 2 * 15)], c=[], cmap=plt.get_cmap('Blues', np.max(arr)-np.min(arr)+1))
        #st.pyplot()

except Exception as e:
    st.info('Waiting for data...')
    st.info(str(e))