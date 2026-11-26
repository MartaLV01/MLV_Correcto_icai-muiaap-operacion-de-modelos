""" DONE-> TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

"""Carga del modelo .joblib y lo usa para predecir la calidad del vino."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import joblib

from model_inference.contracts import WineQualityPrediction
from model_inference.preprocess import FEATURE_NAMES, PREPROCESSING_VERSION, WineFeatures

DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "wine_quality_classifier.joblib"
)

"""
__file__ representa el archivo Python actual, es decir, inference.py.
.resolve() obtiene su ruta absoluta.
.parents[2] sube dos niveles desde el directorio que contiene inference.py hasta la carpeta starter
Despues entra en model y accede al joblib
"""


def load_wine_quality_model(path: Path = DEFAULT_MODEL_PATH) -> dict[str, Any]: #por defecto path es default_model_path
    """Carga el artefacto y comprueba que sea compatible."""

    path = Path(path)

    #comprueba que el archivo existe
    if not path.is_file():
        raise FileNotFoundError(f"No existe el modelo: {path}")
    
    #se carga el modelo
    bundle = joblib.load(path)

    #comprobamos que bundle sea un diccionario con Mapping
    if not isinstance(bundle, Mapping):
        raise ValueError("El artefacto debe ser un diccionario.")

    #comprueba que se tienen los datos que se necesitan para la prediccion
    for key in ("estimator", "feature_names", "model_version"):
        if key not in bundle:
            raise ValueError(f"Falta la clave '{key}' en el artefacto.")

    #comprobamos que el orden de las varibales es el correcto, para ello se pasa el bundle features a tupla
    if tuple(bundle["feature_names"]) != FEATURE_NAMES:
        raise ValueError(
            "Los feature_names del modelo no coinciden con FEATURE_NAMES."
        )

    #se comprueba que la version sea una cadena y no este vacia
    model_version = bundle["model_version"]
    if not isinstance(model_version, str) or not model_version.strip():
        raise ValueError("model_version debe ser una cadena no vacía.")

    #se comprueba que el modelo tenga los metodos que necesitamos
    # getattr() intenta obtener el método 
    # callable() comprueba que lo obtenido se puede llamar como una función.
    estimator = bundle["estimator"]
    if not (
        callable(getattr(estimator, "predict", None))
        and callable(getattr(estimator, "predict_proba", None))
    ):
        raise ValueError(
            "El artefacto no contiene un clasificador compatible."
        )

    # se devuelve bundle como diccionario
    return dict(bundle)


def infer_wine_quality(bundle: Mapping[str, Any], features: WineFeatures, sample_id: str) -> WineQualityPrediction:
    """Predice la categoría de calidad de una muestra preprocesada."""

    estimator = bundle["estimator"]
    # caracteristicas del vino (preprocess).
    # En [], para que siempre sea una lista
    x = [features.as_vector()] 

    label = str(estimator.predict(x)[0])
    confidence = float(max(estimator.predict_proba(x)[0]))

    return WineQualityPrediction(
        sample_id=sample_id,
        quality_band=label,
        confidence=round(confidence, 2),
        model_version=bundle["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )