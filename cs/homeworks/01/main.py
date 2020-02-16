from bool_solver import BoolStringSolver
import streamlit as st 

eq_str = st.text_input('Equation to solve', value='(x_1 or x_2 and x_3) & (x_4 | x_1) and not x_5')
num = st.slider('Number of variables', 1, len(eq_str))

st.success(f'Total number of decisions: {BoolStringSolver.solve_string(eq_str, num)}')