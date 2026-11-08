import streamlit as st
st.title("Contador con estado")
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Sumar"):
    st.session_state.count += 1
st.metric("Cuenta", st.session_state.count)

"""
sesion_state es un varibale de streamlit que ya esta implementada.
es una variable que se usa para almacenar el estado de 
    todas tus varibales de tu codigo, es como un diccionario global de tu codigo

"""