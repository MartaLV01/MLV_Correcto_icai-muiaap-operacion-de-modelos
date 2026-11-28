from dataclasses import asdict

from fastapi import APIRouter, Body
from typing import Annotated

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import VALID_FEATURES_EXAMPLE, ErrorResponse, Prediction, PredictionRequest, PredictionResponse

# DONE -> TODO S9.3a: mueve aquí `prefix="/v1/predictions"` y `tags=["predictions"]`.
# DONE -> TODO S9.3c: declara a nivel de router `responses=` para 400, 422 y 503 con
# `{"model": ErrorResponse, "description": ...}`. Así el 422 deja de
# documentarse como `HTTPValidationError`, que ya no es lo que devolvemos.
# router = APIRouter() # ORIGINAL

# prefix -> establece la parte común de la URL para todas las rutas del router.
# tags -> agrupa los endpoints bajo la categoría predictions en Swagger
# @router.post("") -> define la ruta raíz dentro de ese prefijo
# los errores s eponen en APIRouter ya que son comunes a las rutas que pertenecen a este router.
router = APIRouter(prefix="/v1/predictions", tags=["predictions"], 
                   responses={
                        400: {
                            "model": ErrorResponse,
                            "description": "El cuerpo del JSON no es valido",
                        },
                        422: {
                            "model": ErrorResponse,
                            "description": "La validacion fallo, los datos no pasaron el contrato",
                        },
                        503: {
                            "model": ErrorResponse,
                            "description": "El modelo no esta preparado",
                        },
                    },
                )

@router.post("",
    response_model=PredictionResponse, # contrato de la respuesta
    summary="Predice la calidad del vino",
    response_description="Prediccion de la calidad del vino",
)

#ORIGINAL
#@router.post("/v1/predictions")
#def create_prediction(
#    payload: PredictionRequest,
#    predictor: PredictorDep,
#    request_id: RequestIdDep,
#):
def create_prediction(
    # payload: PredictionRequest,
    payload: Annotated[
        PredictionRequest,
        Body(
            openapi_examples={ # son los nombres que tiene el test, al hacer el assert
                "valid": {
                    "summary": "Petición válida",
                    "description": "Ejemplo de una petición con todas las características del vino dentro de los rangos permitidos.",
                    "value": {
                        "features": VALID_FEATURES_EXAMPLE
                    },
                },
                "invalid_range": {
                    "summary": "Acidez fija fuera de rango",
                    "description": "Ejemplo de una petición con un valor de acidez fija no permitido.",
                    "value": {
                        "features": {
                            **VALID_FEATURES_EXAMPLE,
                            "fixed_acidity": -1.0,
                        }
                    },
                },
                "invalid_type": {
                    "summary": "Dato con tipo incorrecto",
                    "description": "Ejemplo de una petición en la que el alcohol se proporciona como texto.",
                    "value": {
                        "features": {
                            **VALID_FEATURES_EXAMPLE,
                            "alcohol": "alto",
                        }
                    },
                },
            }
        ),
    ],
    predictor: PredictorDep,
    request_id: RequestIdDep,
) -> PredictionResponse:

    """Predice la calidad del vino a partir de sus características.

    La respuesta incluye:
    - La categoría de calidad predicha
    - La confianza de la predicción, entre 0 y 1, redondeada a dos decimales
    - La versión del modelo y del preprocesamiento
    - El identificador de la petición y la fecha y hora de respuesta
    """
    
    # DONE -> TODO S9.3e: añade summary, response_description y un docstring útil para
    # quien consume la API (campos, rangos, decimales de confidence).
    # DONE -> TODO S9.3f: ofrece en Swagger al menos tres ejemplos de cuerpo (uno válido
    # y dos inválidos). Investiga `Annotated[PredictionRequest, Body(...)]` con
    # `openapi_examples=`; usa VALID_FEATURES_EXAMPLE como base.
    output = predictor.predict(payload.features) # output -< ModelOutput

    # DONE -> TODO S9.1e: este dict expone `raw_score` y la confianza sin redondear.
    # Declara `-> PredictionResponse` y construye el modelo; para pasar de la
    # dataclass ModelOutput a Prediction investiga `from_attributes=True`.

    # from_attributes=True permite a Pydantic leer los atributos
    # de un objeto Python para construir un modelo

    #ORIGINAL
    #return {"prediction": asdict(output), "request_id": request_id}
    prediction = Prediction.model_validate(output)
    return PredictionResponse(prediction= prediction, request_id= request_id)
