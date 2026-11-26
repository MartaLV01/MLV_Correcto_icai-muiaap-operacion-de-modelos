from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

# Creamos el router donde registraremos nuestro endpoint.
router = APIRouter()


# DONE -> TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)

# con el decorador decimos que la funcion responde a 
# peticiones d etipo POST
# en la ruta /predict
# al hacer response_model=PrediccionSalida se le indica que 
# la respuesta debe ajustarse al modelo PrediccionSalida
# entrada: PrestamoEntrada -> FastAPI interpreta que debe 
# recibir un cuerpo JSON y validarlo utilizando PrestamoEntrada
@router.post("/predict", response_model=PrediccionSalida)
def predict(entrada: PrestamoEntrada):
    return predecir(entrada)
