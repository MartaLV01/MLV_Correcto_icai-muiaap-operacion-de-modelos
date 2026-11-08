"""DONE-> TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.


from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class WineQualityRequest(BaseModel):
    """Variables de la muestra vino. Estructura que debe seguir los datos de netrada"""

    model_config = ConfigDict(extra="forbid") #prohibo varibles extra

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=2)
    residual_sugar: float = Field(ge=0, le=20)
    chlorides: float = Field(ge=0, le=1)
    free_sulfur_dioxide: float = Field(ge=0, le=100)
    total_sulfur_dioxide: float = Field(ge=0, le=300)
    density: float = Field(ge=0.98, le=1.01)
    ph: float = Field(ge=2.5, le=4.5)
    sulphates: float = Field(ge=0, le=3)
    alcohol: float = Field(ge=5, le=20)

class WineQualityPrediction(BaseModel):
    """Estructura de la prediccion (salida)"""
    model_config = ConfigDict(extra="forbid", frozen=True)

    sample_id: str = Field(min_length=1)
    quality_band: Literal["acceptable", "excellent", "needs_review"]
    confidence: float = Field(ge=0.00, le=1.00)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)

class HealthResponse(BaseModel):
    """Estado mínimo del servicio y versión del artefacto cargado."""

    status: Literal["ok"]
    model_version: str