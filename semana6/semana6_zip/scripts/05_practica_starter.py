import streamlit as st
from modelo import predict_toy

st.set_page_config(page_title="Churn con memoria", layout="centered") # indica el nombre de la pagina
st.title("Churn con memoria") # titulo
st.caption("Regla de juguete. No usar para tomar decisiones sobre clientes.") # informacion adicional

# A: iniciar el historial una sola vez, no en cada rerun.
if "history" not in st.session_state:
    # cuando el user interactua con la pagina streamlit vuelve a rerunearse por lo que se puedne perder datos
    # para evitarlo se usa st.session_state
    # ademas con el if comprueba si hay un historial y si no lo crea. 
    # Se evita que se pierda al crearse con cada rerun
    st.session_state.history = []
    #pass  # DONE -> TODO A: asignar [] a st.session_state.history

def submit_prediction():
    # Leer los valores nuevos desde las keys, no mediante args del callback.
    inputs = {name: st.session_state[name] for name in
              ("tenure_months", "monthly_spend_eur", "contract", "support_calls")}
    result = predict_toy(**inputs) # mi funcion del model.py
    # B: una fila por submit. No predecir en cada rerun.
    st.session_state.history.append({**inputs, **result}) # se añade el input y resultado a la historia

    #pass  # DONE -> TODO B: añadir {**inputs, **result} a history

# limpia el historial solo si es llamada
def clear_history():
    st.session_state.history = []

# se crea el fomrulario
with st.form("churn_form"):
    # key permite recupeerear el valor usando st.session_state["nombre key"]
    # es una barra deslizante de 0 a 72, por defectop empieza en 6
    st.slider("Antigüedad (meses)", 0, 72, 6, key="tenure_months") 
    # permite introducir un nuemro, min 0 max 200. por defecto empieza en 80. el incremento es de  5 en 5
    st.number_input("Gasto mensual (EUR)", 0.0, 200.0, 80.0,
                    step=5.0, key="monthly_spend_eur")
    # es un desplegable
    st.selectbox("Contrato", ["Mensual", "Anual"], key="contract")
    st.slider("Llamadas a soporte", 0, 5, 2, key="support_calls")
    # se crea el boton. Solo se predice cuando el user lo pulsa
    # on_click=submit_prediction sin parentesis ya que asi solo se ejecuta si el user lo pulsa, 
    # en caso contrario se ejecuta antes de pulsarlo
    st.form_submit_button("Predecir y guardar", on_click=submit_prediction)

# Fuera del form: provoca rerun sin añadir otra predicción.
st.checkbox("Mostrar ayuda", key="show_help") # crea una casilla que se puede [des]marcar
if st.session_state.show_help: # al pulsar la casilla se muestra este mensaje
    st.info("El form envía todos sus valores al pulsar submit. El historial vive en esta sesión.")

# C: mostrar un contador y, si hay filas, st.dataframe.
# Pista: history = st.session_state.get("history", [])
st.info("DONE -> TODO C: dibuja aquí el historial y su contador.")
# un indicador numerico. numeor de predicciones que se llevan hechas
st.metric("Predicciones guardadas", len(st.session_state.history)) 
if st.session_state.history: # mira si la lista esta vacia o no
    last = st.session_state.history[-1] # obtiene el ultima elemneto calculado (ya que es el que se quiere mostrar, el resto ya esta mostrandose)
    # muestra en verde el % de la ultima prediccion + su riesgo
    st.success(f"Último riesgo: {last['risk']} ({last['probability']:.0%})") 
    # muestra toda la tabla de predicciones
    st.dataframe(st.session_state.history, hide_index=True, width="stretch")
else:
    st.info("Aún no has enviado ninguna predicción.")

# solo cuando el user pulsa el boton el historial se vacia
st.button("Vaciar historial", on_click=clear_history)
st.caption("Recargar el navegador o cerrar la conexión puede borrar la sesión. No es una base de datos.")
