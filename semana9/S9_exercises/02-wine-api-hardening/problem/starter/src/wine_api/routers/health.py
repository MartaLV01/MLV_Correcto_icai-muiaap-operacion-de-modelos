from fastapi import APIRouter, HTTPException

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import ErrorResponse, HealthResponse  # noqa: F401 - pista para S9.1d
from wine_api.errors import ModelUnavailableError

SERVICE_NAME = "wine-quality-prediction"

# DONE -> TODO S9.3a: declara `tags=["health"]` en el router, no en include_router().
# router = APIRouter() # ORIGINAL
router = APIRouter(tags=["health"])

# DONE -> TODO S9.3b: añade `summary=`, `response_description=` y un docstring que diga
# cuándo usar el endpoint y qué significa un 503. Documenta el 503 con
# `responses={503: {"model": ErrorResponse, "description": ...}}`.
# @router.get("/health") # ORIGINAL
@router.get(
    "/health",
    summary="Check API and model health",
    response_description="Health status of the API and prediction model",
    responses={
        503: {
            "model": ErrorResponse,
            "description": "The prediction model is not ready",
        }
    },
)
#def read_health(predictor: PredictorDep, request_id: RequestIdDep): #ORIGINAL
def read_health(predictor: PredictorDep, request_id: RequestIdDep) -> HealthResponse:
    """
    Mira que la API y la prediccion del modelos sean correctos
    Usa este endpoitn para checkeos
    Devuelve 503 si la prediccion no esta bien
    """

    # DONE -> TODO S9.2f: sustituye el HTTPException por `ModelUnavailableError`: el
    # dominio no debería saber de HTTP y el manejador produce el sobre común.
    if not predictor.is_ready():
        # raise HTTPException(status_code=503, detail="Model not ready") #ORIGINAL
        # Usamos nuestra exception
        # no necesitamos los argumentos porque ya estan deficnidos en la exception
        raise ModelUnavailableError() 
    
    #DONE -> TODO S9.1d: declara `-> HealthResponse` y devuelve una instancia.
    #ORIGINAL
    #return {
    #    "status": "ok",
    #    "service": SERVICE_NAME,
    #    "model_status": "ready",
    #    "model_version": predictor.model_version,
    #    "request_id": request_id,
    #}
    # no queremos devolver un diccionario si no una instancia de python
    # segun el contrato de schemas 
    return HealthResponse(
        status = "ok",
        service = SERVICE_NAME,
        model_status = "ready",
        model_version = predictor.model_version,
        request_id = request_id,
    )