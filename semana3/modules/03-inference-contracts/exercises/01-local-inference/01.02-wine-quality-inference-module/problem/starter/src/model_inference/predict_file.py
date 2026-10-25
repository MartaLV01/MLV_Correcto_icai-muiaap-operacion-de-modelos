"""DONE -> TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.


import argparse
import csv
import tempfile
from pathlib import Path

from pydantic import ValidationError

from model_inference.contracts import WineQualityRequest
from model_inference.inference import DEFAULT_MODEL_PATH, infer_wine_quality, load_wine_quality_model
from model_inference.preprocess import preprocess_wine_request

#Que es lo que quiero que el csv de salida tenga
OUTPUT_FIELDS = (
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
)


def predict_file(input_path: Path, output_path: Path, model_path: Path) -> int:
    """Valida las filas, predice y escribe el CSV de salida."""

    # Se carga el modelo
    model = load_wine_quality_model(model_path)

    # Se lee el csv
    # Se guardan las predicciones antes de escribir el resultado.
    predictions = []

    with input_path.open(newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source) #pasa el csv a diccionario

        # si sample id no esta en el csv (diccionario) o no tiene campos da error
        if not rows.fieldnames or "sample_id" not in rows.fieldnames:
            raise ValueError("El CSV de entrada debe incluir una columna sample_id.")

        # recorre cad auna de la filas del diccionario (csv)
        # se empieza en 2 ya que la primera fila son los nombre de las columnas
        for row_number, row in enumerate(rows, start=2):
            # consigue el sample id (identificador) del diccionario y lo elimina de el
            # ya que en el contrato no lo hemos definido, ademas hemos dicho que no deje columnas de mas
            # asique si dejaramos el sample_id daria error
            sample_id = row.pop("sample_id", None)

            # ademas comprobamos que el identificador no este vacio
            if not isinstance(sample_id, str) or not sample_id.strip():
                raise ValueError(f"La fila {row_number} tiene un sample_id vacío.")

            try:
                # Se validan los datos de entrada con nuestro contrato
                request = WineQualityRequest.model_validate(row)

                # Pasamos los datos validados a nuestro objeto WineFeatures
                features = preprocess_wine_request(request)

                # Se hace la prediccion
                prediction = infer_wine_quality(model, features, sample_id)

            # se capturan los errroes que pudieran haber
            except ValidationError as error:
                raise ValueError(
                    f"Fila {row_number} inválida "
                    f"(sample_id={sample_id}): {error}"
                ) from error

            # se añade la prediccion a la lista de predicciones, no en nuestro archivo final de salida
            # se hace en una lista y no en nuestro archivo de salida para que si hay cualquier error 
            # no se tenga un archivo incompleto
            predictions.append(prediction.model_dump())

    # Solo se ejecuta si no ha habido error al hacer el preprocesamiento o las predicciones
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None

    try:
        # Creamos un archivo temporal en la misma carpeta que el destino.
        with tempfile.NamedTemporaryFile(
            mode="w", #se abre en modo escritura (w)
            newline="",
            encoding="utf-8",
            dir=output_path.parent, # que el temporal se cree en la carpeta donde estara el resultado fianl
            # sufijo y prefijo se usan para que se cree con un nombre reconocible de que es temporal
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False, # evita que se borre automaticamnete al salir del with
        ) as target:
            # se guarda la dir del archivo temporal
            temporary_path = Path(target.name)

            # se escribe en el archivo temporal las predicciones y el nombre de las columnas
            # segun mis condiciones de salida
            writer = csv.DictWriter(target, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(predictions)

        # Sustituimos el destino solo cuando el CSV está completo.
        # el replace sustituye el archivo de destino (outputpath) por el de origen (temporary path) (mantiene nombre de destino)
        temporary_path.replace(output_path)
        temporary_path = None 
        # se indica que ya no hay un archivo temporal. 
        # Se indica para que no entre ne el if del finally, 
        # en donde se borra el temporal si ha habido errores en la escritura

    # no se captura aqui el error con el except ya que en el main es donde lo estamos capturando
    finally:
        # Si falla la escritura, se borra el archivo temporal.
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return len(predictions)


def parse_args() -> argparse.Namespace:
    """Define los argumentos del comando."""

    # para poder ejecutar: 
    # python -m model_inference.predict_file --input assets/inference_samples.csv --output predictions.csv
    # indicar el path del modelo es opcional
    parser = argparse.ArgumentParser(description="Inferencia local de calidad de vino")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, type=Path)

    return parser.parse_args()


def main() -> int:
    """Ejecuta la inferencia desde la línea de comandos."""

    # obtiene los argumantos de nuestro input
    arguments = parse_args()

    # trata de hacer la prediccion
    try:
        prediction_count = predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            model_path=arguments.model,
        )
    except (FileNotFoundError, ValueError, OSError) as error:
        raise SystemExit(f"Error: {error}") from error

    print(f"Predicciones escritas: {prediction_count}")
    return 0

# permite ejecutar el módulo desde la terminal. 
# main() coordina la ejecución
# SystemExit comunica el código de salida al sistema operativo.
if __name__ == "__main__":
    raise SystemExit(main())
