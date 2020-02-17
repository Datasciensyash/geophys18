from bool_solver import BoolStringSolver
import re
import streamlit as st 

eq_str = st.text_input('Equation to solve', value='(x_1 or x_2 and x_3) & (x_4 | x_1) and not x_5')
var = set(re.findall(r'\w_\d', eq_str))
st.info('Founded valriables: ' + str(var))

num, df = BoolStringSolver.solve_string(eq_str, len(var), var)
st.success(f'Total number of decisions: {num}')
st.table(df) #st.dataframe(df)