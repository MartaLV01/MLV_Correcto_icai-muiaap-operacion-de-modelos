"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from pathlib import Path

from pydantic import ValidationError

from model_packaging.artifact import DEFAULT_BUNDLE_PATH, load_model_bundle, infer_wine_quality
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""
    
    # Validar el bundle antes de procesar las filas
    bundle = load_model_bundle(bundle_path)

    # Comprobar que existe el CSV de entrada
    if not input_path.is_file():
        raise FileNotFoundError(f"No existe el CSV de entrada: {input_path}")

    if input_path.resolve() == output_path.resolve():
        raise ValueError("El fichero de salida no puede ser el mismo que el fichero de entrada")

    output_rows = []

    # Leer y validar todo el CSV
    with input_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        # El orden de las columnas forma parte del contrato
        if reader.fieldnames != list(FEATURE_NAMES):
            raise ValueError(f"El encabezado del CSV no es el esperado\nSe esperaba: {list(FEATURE_NAMES)}\nSe recibió: {reader.fieldnames}")

        # Procesar todas las filas sin escribir el CSV final
        # start = 2 para indicar que es la linea 2 del csv ya que la 1 tiene el encabezado
        for row_number, row in enumerate(reader, start=2):
            try:
                request = WineQualityRequest.model_validate(row) # del diccionario a objeto WineQualityRequest
                prediction = infer_wine_quality(bundle, request) # se hace la predccion

            except (ValidationError, ValueError, TypeError) as exc:
                raise ValueError(f"Error en la fila {row_number} del CSV: {exc}") from exc 
                # from exc pasa tambien el mensaje original del error

            # Conservar los datos originales y añadir el resultado
            output_rows.append({
                **row,
                "quality_band": prediction.quality_band,
                "confidence": prediction.confidence,
                "model_version": prediction.model_version,
                "preprocessing_version": (prediction.preprocessing_version),
            })

    # Si no hay filas de entrada no se crea un csv de salida
    if not output_rows:
        raise ValueError("El CSV de entrada no contiene filas de datos")

    # Solo llegamos aquí si todas las filas han sido válidas
    # crea la carpeta de salida
    # parents=True permite crear también las carpetas superiores que no existan.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # crea el encabezado del csv de salida
    fieldnames = [
        *FEATURE_NAMES, #desempaqueta los nombres dentro de la lista
        "quality_band",
        "confidence",
        "model_version",
        "preprocessing_version",
    ]

    temporary_path = None

    try:
        # Crear el temporal en la misma carpeta que la salida, para que si hay algun error no se haya creado el csv final
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=output_path.parent,
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            
            temporary_path = Path(temporary_file.name)
            # escribo el csv temporal
            writer = csv.DictWriter(
                temporary_file,
                fieldnames=fieldnames,
            )
            writer.writeheader() # cabeceras
            writer.writerows(output_rows) # columnas

            # Asegurar que los datos llegan al sistema de archivos
            temporary_file.flush() # vacía los datos pendientes del búfer de Python hacia el sistema operativo
            os.fsync(temporary_file.fileno()) # solicita al sistema operativo que sincronice los datos del archivo con el almacenamiento

        # Publicar el resultado cuando el temporal está completo
        os.replace(temporary_path, output_path) # reemplaza el archivo de destino por el temporal
        temporary_path = None # para indicar que ya no debemos intentar eliminar ese temporal

    finally:
        # Limpiar el temporal si se produce un error
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return len(output_rows)

    # raise NotImplementedError("Implementa predict_file().")


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
