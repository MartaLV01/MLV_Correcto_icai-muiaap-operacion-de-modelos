"""Punto de entrada de la API: `fastapi dev` usa `wine_api.main:app`."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wine_api.errors import install_error_handlers
from wine_api.predictor import Predictor, build_predictor
from wine_api.request_id import request_id_middleware
from wine_api.routers import health, predictions

# DONE -> TODO S9.3g: completa los metadatos que lee el consumidor en /docs:
# `version` (¿mayor, menor o parche tras S9.1c?), `summary`, una `description`
# en Markdown que explique `request_id` y el sobre de error, y `openapi_tags`
# con una descripción por tag. Comprobación: tests/test_s9_3_openapi.py
# API_VERSION = "1.0.0" #ORIGIANL
API_VERSION = "1.1.0" 
# psas a ser esta version por ql cambio en 9.1 al añadir served_at -> cambio comptatible

API_SUMMARY = "API para predecir la calidad de vinos tintos"
API_DESCRIPTION = """
        ## Descripción

        Esta API permite obtener predicciones sobre la calidad de vinos tintos
        a partir de sus características fisicoquímicas

        ### Identificador de petición (`request_id`)

        Cada petición recibe un id único (`request_id`)
        Este id aparece en las respuestas y permite relacionar
        las peticiones con los registros de la aplicación

        ### Formato de errores

        Todas las respuestas de error siguen un formato común:

        - `error.code`: código estable que identifica el tipo de error
        - `error.message`: descripción del error
        - `error.fields`: información adicional sobre los campos que han fallado
        en la validación, cuando corresponda
        - `request_id`: identificador de la petición que ha producido el error
        """

OPENAPI_TAGS = [
        {
            "name": "health",
            "description": "Comprobación del estado de la API y de la disponibilidad del modelo.",
        },
        {
            "name": "predictions",
            "description": "Operaciones para predecir la calidad de los vinos a partir de sus características.",
        },
    ]

def create_app(predictor: Predictor | None = None) -> FastAPI:
    """Crea la aplicación; los tests inyectan su propio predictor."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.predictor = predictor or build_predictor(
            os.environ.get("WINE_API_MODE", "ready")
        )
        yield

    app = FastAPI(title="Wine Quality API", version=API_VERSION, 
                summary=API_SUMMARY, description=API_DESCRIPTION, openapi_tags=OPENAPI_TAGS,
                lifespan=lifespan)
    app.middleware("http")(request_id_middleware)
    install_error_handlers(app)
    app.include_router(health.router)
    app.include_router(predictions.router)
    return app


app = create_app()
