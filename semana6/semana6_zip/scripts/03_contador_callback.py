import streamlit as st
st.title("Contador con callback")
if "count" not in st.session_state:
    st.session_state.count = 0
def increment():
    st.session_state.count += 1
st.button("Sumar", on_click=increment)
st.metric("Cuenta", st.session_state.count)

#Estyo no estaba pero en eñl suyo si
#st.text_input('Name', key='name')

#def set_name(name):
#    st.session_state.name = name
#st.button("calera name", on_click=set_name, args=[""])
#st.button("Streamlit!", on_click=set_name, args=["Streamlit"]) #al pusar este boton se llama a set nema con el nombre=straemlit, se cambia el nombre

