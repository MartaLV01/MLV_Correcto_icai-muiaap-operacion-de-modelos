"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Self

import joblib
import math
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

from model_packaging.preprocess import(
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    preprocess_wine_request
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""


class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1) # comprueba que no esta vacio
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_contract(self) -> Self:

        if self.schema_version != ARTIFACT_SCHEMA_VERSION:
            raise ValueError(f"Versión de esquema incompatible. \nEsperado: {ARTIFACT_SCHEMA_VERSION}. \nRecibido: {self.schema_version}")

        if self.preprocessing_version != PREPROCESSING_VERSION:
            raise ValueError(f"Versión del preprocesado incompatible. \nEsperado: {PREPROCESSING_VERSION}. \nRecibido: {self.preprocessing_version}")

        if self.feature_names != FEATURE_NAMES:
            raise ValueError(f"Las características o su orden son incompatibles. Deben ser y seguir este orden: \n{FEATURE_NAMES} \nSe recibió: {self.feature_names}")

        if self.output_labels != OUTPUT_LABELS:
            raise ValueError(f"Las etiquetas de salida deben de ser:\n{OUTPUT_LABELS}")

        return self



@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """DONE -> TODO: devuelve un manifiesto compatible con el contrato."""

    # Comprueba que no esta vacio
    if not model_version.strip():
        raise ValueError("model_version no puede estar vacío")

    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version=PREPROCESSING_VERSION,
        feature_names=FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__,
    )

    # raise NotImplementedError("Implementa create_manifest().")


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """DONE -> TODO: escribe manifest.json y model.joblib de forma segura."""

    # como se le puede pasar o no manifiesto (ArtifactManifest | None = None), si no lo hay se crea
    if manifest is None:
        manifest = create_manifest(
            estimator,
            model_version="wine-quality-rf-v1",
        )

    # Comprueba que el estimador y el manifiesto coinciden.
    if type(estimator).__name__ != manifest.estimator_type:
        raise ValueError(f"El tipo de estimador {type(estimator).__name__} no coincide con el manifiesto {manifest.estimator_type}")

    # Crea la carpeta si todavía no existe.
    bundle_path.mkdir(parents=True, exist_ok=True)

    model_path = bundle_path / MODEL_FILENAME
    manifest_path = bundle_path / MANIFEST_FILENAME

    # Guarda el modelo.
    joblib.dump(estimator, model_path)

    # Guarda el manifiesto como JSON legible.
    manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")

    return manifest

    # raise NotImplementedError("Implementa save_model_bundle().")


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """DONE -> TODO: valida el manifiesto antes de cargar el estimador."""

    # se crean las rutas con el bundle_path
    manifest_path = bundle_path / MANIFEST_FILENAME
    model_path = bundle_path / MODEL_FILENAME

    # Se comprueba que esas rutas existen
    if not bundle_path.is_dir():
        raise FileNotFoundError(f"No existe la carpeta del bundle: {bundle_path}")

    if not manifest_path.is_file():
        raise FileNotFoundError(f"No existe el manifiesto: {manifest_path}")

    if not model_path.is_file():
        raise FileNotFoundError(f"No existe el modelo: {model_path}")

    # Primero se lee y valida el JSON para que sea de tipo ArtifactManifest.
    try:
        manifest = ArtifactManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ValueError(f"El manifiesto es inválido: {exc}") from exc

    # Solo después de validar el manifiesto se carga el modelo.
    estimator = joblib.load(model_path)

    if type(estimator).__name__ != manifest.estimator_type:
        raise ValueError(f"El tipo de estimador ({type(estimator).__name__}) no coincide con el manifiesto: {manifest.estimator_type}")

    if not callable(getattr(estimator, "predict", None)):
        raise TypeError("El estimador(modelo) no implementa predict()")

    if not callable(getattr(estimator, "predict_proba", None)):
        raise TypeError("El estimador(modelo) no implementa predict_proba()")

    # devulevo el modelo cargado
    return LoadedModelBundle(estimator=estimator, manifest=manifest)

    # raise NotImplementedError("Implementa load_model_bundle().")


def infer_wine_quality(bundle: LoadedModelBundle, request: WineQualityRequest) -> WineQualityPrediction:
    """DONE -> TODO: preprocesa, invoca el estimador y valida la respuesta."""

    # Preprocesamiento (preprocess.py)
    features = preprocess_wine_request(request)
    vector = features.as_vector() # una muestra con 11 características

    # El estimador espera una matriz -> una fila de muestras y once columnas de features.
    matrix = [vector]

    # Obtener las predicciones
    predictions = bundle.estimator.predict(matrix)

    if len(predictions) != 1:
        raise ValueError("El estimador (modelo) debe devolver solo una prediccion por petición (muestra)")

    quality_band = predictions[0]

    # Validar la salida.
    if quality_band not in OUTPUT_LABELS:
        # !r indica que se escriba entre '', si es una cadena vacia sera mas facil de identificar
        raise ValueError(f"El estimador ha devuelto la etiqueta {quality_band!r}, que no está entre las etiquetas permitidas: {OUTPUT_LABELS}")

    # Obtener las probabilidades de la prediccion hecha
    probabilities = bundle.estimator.predict_proba(matrix)

    if len(probabilities) != 1:
        raise ValueError("El estimador (modelo) debe devolver probabilidades para una petición (muestra)")

    row_probabilities = probabilities[0]

    if len(row_probabilities) != len(bundle.manifest.output_labels):
        raise ValueError("El número de probabilidades no coincide con el número de etiquetas del manifiesto")

    # Comprobar que las probabilidades son válidas
    values = [float(value) for value in row_probabilities]

    # comprueba que la probabilidad sea un valor finito y este entre 0 y 1
    # Cuando todas las comprobaciones sean true devuelve true 
    if not all(
        math.isfinite(value) and 0 <= value <= 1
        for value in values
    ):
        raise ValueError("El estimador ha devuelto probabilidades no finitas o fuera del intervalo [0, 1].")

    # La confianza será la probabilidad de la etiqueta predicha
    label_index = bundle.manifest.output_labels.index(quality_band)
    confidence = values[label_index]

    # 7. Construir la respuesta mediante el contrato.
    return WineQualityPrediction(
        quality_band=quality_band,
        confidence=confidence,
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version,
    )

    # raise NotImplementedError("Implementa infer_wine_quality().")
