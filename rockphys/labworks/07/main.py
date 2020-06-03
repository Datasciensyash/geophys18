from modules import find_outliers
import modules

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

data_raw = st.text_input('Данные:', value='15, 15, 16, 19, 70, 55, 30, 20, 16, 16, 18, 20, 600, 40, 100, 25, 38, 18, 15, 17, 29')
data = np.array(eval('[' + data_raw + ']')) #That is bad.

delta = st.slider('Delta modifier', 1., 5., value=3.0, step=0.1)

lower, upper, distribution, etc, ro_average, delta_sigma = find_outliers(data, delta)

distribution_false = modules.get_distribution(data, modules.get_step_num(data), step_size=modules.get_step_size(data, modules.get_step_num(data)))
print(distribution_false)
colors = ['g' if i else 'r' for i in (data >= lower) & (data <= upper)]

#colors_bar = ['g' if i else 'r' for i in (data >= lower) & (data <= upper)]
x = [i for i in range(len(distribution_false))]
plt.bar(x, distribution_false, label='Все измерения')#, color=colors)
plt.xticks(x, [f'{round(np.min(data) + modules.get_step_size(data, modules.get_step_num(data)) * i, 1)} - {round(np.min(data) + modules.get_step_size(data, modules.get_step_num(data)) * (i + 1), 1)}' for i in x], rotation=16, size=7)
plt.xlabel("Интенсивность гамма-измерения, Iγ")
plt.ylabel("Количество измерений, N")
plt.legend()
st.pyplot()
plt.cla()

colors = ['g' if i else 'r' for i in (data >= lower) & (data <= upper)]

x = [i for i in range(len(distribution))]
plt.bar(x, distribution, label='Не аномальные измерения')
plt.xticks(x, [f'{round(etc[3] + etc[2] * i, 1)} - {round(etc[3] + etc[2] * (i + 1), 1)}' for i in x], rotation=16, size=7)
plt.xlabel("Интенсивность гамма-измерения, Iγ")
plt.ylabel("Количество измерений, N")
plt.legend()
st.pyplot()
plt.cla()

plt.scatter([i for i in range(len(data))], data, c=colors, label="Измерения")
plt.axhline(upper, c='r', label=f'Iγ_min (аномальная): {round(upper, 4)}')

plt.xlabel("Номер измерения, n")
plt.ylabel("Интенсивность гамма-излучения, Iγ")
plt.legend(fontsize='x-small')
plt.savefig('./images/full.png')
st.pyplot()

with open('info.md', 'a', encoding='utf-8') as f:
	f.write('--- \n\n')
	f.write('## Статистика \n\n')
	f.write(f'Минимальная аномальная Интенсивность: `{upper}` \n\n')

	f.write(f'![Illustration](https://github.com/Datasciensyash/geophys18/raw/master/rockphys/labworks/07/images/full.png) \n\n')

	pickets = [i for i in np.argwhere(np.array(data) > upper).T[0].tolist()]
	strp = ''
	for i in pickets:
		strp += f'`{i}`, '


	f.write(f'Аномалии (Номера пикетов): {strp} \n\n' )

st.info(f'Аномалии (Номера пикетов): {np.argwhere(np.array(data) > upper).T}')