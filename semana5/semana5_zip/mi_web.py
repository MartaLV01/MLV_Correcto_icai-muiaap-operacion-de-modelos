# ESTO ES UN EJEMPLO. LOS DATOS SON INVENTADOS

"""
import streamlit as st

st.set_page_config(page_title="CV") # da nombre a la pestaña
#st.title("Escribe tu nombre") 

st.markdown(
    ""
    <div style="
        background-color: #1e293b;
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 50px;
        font-weight: bold;
        text-align: left;
    ">
        Escribe tu nombre
    </div>
    "",
    unsafe_allow_html=True
)
#st.caption("Churn sintético · ejemplo docente")
st.header("Abaout me")
st.text("Escribe sobre tus ambiciones/gustos/....")
st.header("Studies")
st.text("Escribe sobre tus ambiciones/gustos/....")
"""


import streamlit as st

# -----------------------------
# Configuración
# -----------------------------
st.set_page_config(
    page_title="Mi CV",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Contenedor principal */
    .cv-container {
        max-width: 1100px;
        margin: auto;
        background-color: white;
        padding: 40px;
        border-radius: 15px;
    }

    /* Nombre */
    .name {
        font-size: 42px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0;
    }

    /* Profesión */
    .profession {
        font-size: 20px;
        color: #2563eb;
        margin-top: 5px;
    }

    /* Títulos */
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #1f2937;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 5px;
        margin-top: 30px;
    }

    /* Experiencia */
    .job {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #2563eb;
    }

    .job-title {
        font-size: 18px;
        font-weight: bold;
    }

    .company {
        color: #2563eb;
        font-weight: bold;
    }

    .date {
        color: #6b7280;
        font-size: 14px;
    }

    /* Skills */
    .skill {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.image(
        "https://via.placeholder.com/150",
        width=150
    )

    st.markdown("## Contacto")

    st.write("📍 Madrid, España")
    st.write("📧 email@example.com")
    st.write("📱 +34 600 000 000")

    st.markdown("### 🔗 Enlaces")

    st.write("[LinkedIn](https://linkedin.com)")
    st.write("[GitHub](https://github.com)")


# -----------------------------
# CV
# -----------------------------

st.markdown('<div class="cv-container">', unsafe_allow_html=True)

# Cabecera
st.markdown(
    '<div class="name">Juan Pérez</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="profession">Data Scientist | Python Developer</div>',
    unsafe_allow_html=True
)

st.write("")

# Sobre mí
st.markdown(
    '<div class="section-title">Sobre mí</div>',
    unsafe_allow_html=True
)

st.write("""
Profesional especializado en análisis de datos y desarrollo de aplicaciones
con Python. Experiencia trabajando con machine learning, automatización y
visualización de datos.
""")


# Experiencia
st.markdown(
    '<div class="section-title">Experiencia</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="job">

<div class="job-title">
Data Scientist
</div>

<div class="company">
Empresa XYZ
</div>

<div class="date">
2023 - Actualmente
</div>

<p>
Desarrollo de modelos de machine learning, análisis de grandes volúmenes
de datos y creación de dashboards interactivos.
</p>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="job">

<div class="job-title">
Python Developer
</div>

<div class="company">
Empresa ABC
</div>

<div class="date">
2021 - 2023
</div>

<p>
Desarrollo de aplicaciones utilizando Python, APIs y bases de datos.
</p>

</div>
""", unsafe_allow_html=True)


# Educación
st.markdown(
    '<div class="section-title">Educación</div>',
    unsafe_allow_html=True
)

st.markdown("""
**Máster en Ciencia de Datos**  
Universidad de Madrid — 2021

**Grado en Ingeniería Informática**  
Universidad de Madrid — 2019
""")


# Skills
st.markdown(
    '<div class="section-title">Habilidades</div>',
    unsafe_allow_html=True
)

skills = [
    "Python",
    "SQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Streamlit",
    "Git",
    "Docker"
]

for skill in skills:
    st.markdown(
        f'<span class="skill">{skill}</span>',
        unsafe_allow_html=True
    )


# Proyectos
st.markdown(
    '<div class="section-title">Proyectos</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Dashboard de ventas")
    st.write(
        "Dashboard interactivo desarrollado con Python y Streamlit."
    )

with col2:
    st.markdown("### 🤖 Modelo predictivo")
    st.write(
        "Modelo de machine learning para predicción de ventas."
    )


st.markdown('</div>', unsafe_allow_html=True)