#ESTO ES SOLO UN EJEMPLO

import streamlit as st

st.title("📄 Mi Curriculum Vitae")
st.write("Es un ejemplo de como se podria ver un CV con streamlit y desplegables")
st.write("La informacion es un ejemplo inventado")

st.header("Juan Pérez")
st.write("Data Analyst | Python Developer")

st.divider()

with st.expander("👤 Información personal"):
    st.write("Edad: 25 años")
    st.write("Ciudad: Madrid")
    st.write("Email: juan@email.com")

with st.expander("🎓 Formación"):
    st.write("Grado en Ingeniería Informática")
    st.write("Universidad XYZ (2020-2024)")

with st.expander("💼 Experiencia laboral"):
    st.write("**Empresa ABC**")
    st.write("Desarrollador Python (2024-2025)")
    st.write("Desarrollo de aplicaciones y análisis de datos.")

with st.expander("🛠️ Habilidades"):
    st.write("- Python")
    st.write("- SQL")
    st.write("- Excel")
    st.write("- Streamlit")

with st.expander("🌍 Idiomas"):
    st.write("- Español: nativo")
    st.write("- Inglés: B2")