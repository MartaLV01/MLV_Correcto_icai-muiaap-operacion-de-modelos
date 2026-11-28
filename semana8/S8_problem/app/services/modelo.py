import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada

# Orden en el que el modelo espera las variables
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

# Variables usadas para decidir el resultado en base a una probabilidad dada
APROBAR = 0.2
REVISAR = 0.5

# DONE -> TODO: cargar el modelo joblib una sola vez, al importar el modulo
model = joblib.load(MODEL_PATH)

# DONE -> TODO: funcion decidir(probabilidad) -> "aprobar", "revisar" o "rechazar" (umbrales en el enunciado)
# Decisión según la probabilidad: menor de 0,2 → aprobar; menor de 0,5 → revisar; resto → rechazar.

def decidir(probabilidad: float) -> str:
    if probabilidad < APROBAR:
        return "aprobar"
    elif probabilidad < REVISAR:
        return "revisar"
    else:
        return "rechazar"

# DONE -> TODO: funcion predecir(entrada) -> PrediccionSalida, usando VARIABLES para ordenar los valores
def predecir(entrada: PrestamoEntrada) -> PrediccionSalida:
    # Ordenar los valores según el orden que espera el modelo
    # seria lo mismo que hacer:
    #   valores = [
    #        entrada.edad,
    #        entrada.ingresos_mensuales,
    #        entrada.importe_prestamo,
    #        entrada.plazo_meses,
    #        entrada.antiguedad_laboral_anios,
    #        entrada.impagos_previos,
    #    ]
    valores = [getattr(entrada, variable) for variable in VARIABLES]
    
    # Obtener la probabilidad de impago -> la daba el enunciado
    # Aunque aqui solo paso un caso, la funcion esta hecha para poder devolver
    # varios casos como una matriz, por eso se indica el [0], para tener el primer valor
    # El [1] indica que queremos el segundo valor del array, el cual es la proba de impago
    # predict_proba devuelve algo como [[], [], ...], donde cada array es una observacion
    # su contenido es la [proba de la clase 0 , proba de la clase 1 ]
    # en nuestro caso 0 -> pago; 1 -> impago (es lo que quweremos)
    probabilidad = model.predict_proba([valores])[0][1]

    # Decidir según los umbrales establecidos
    decision = decidir(probabilidad)

    # Devolver el resultado validado por Pydantic
    return PrediccionSalida(
        probabilidad_impago=float(probabilidad),
        decision=decision
    )