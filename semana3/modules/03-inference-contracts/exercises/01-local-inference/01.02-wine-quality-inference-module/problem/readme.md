# Problema — Construir un módulo local de inferencia

Trabajad únicamente en `starter/`; esa carpeta es el proyecto que recibe el
alumnado. El artefacto preentrenado se entrega aparte como
`models/wine_quality_classifier.joblib`.

```bash
cd starter
uv sync
uv run pytest
```

Las pruebas empezarán rojas. Implementad los archivos en este orden:

1. `contracts.py`: petición validada y predicción de salida.
2. `preprocess.py`: vector con las 11 características en orden estable.
3. `inference.py`: carga y validación del artefacto, más predicción.
4. `predict_file.py`: entrada CSV, cadena de inferencia y CSV de salida.

El `.joblib` contiene un diccionario con `estimator`, `feature_names` y
`model_version`. El cargador debe comprobar que `feature_names` coincide con
`FEATURE_NAMES` antes de hacer una predicción.

El comando final debe ser:

```bash
uv run python -m model_inference.predict_file \
  --input assets/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

No consultéis la carpeta `solutions/` hasta el debrief.


## Nota sobre el entorno virtual y la ejecución de las pruebas

### Problema encontrado

Al ejecutar uv sync y posteriormente las instrucciones del ejercicio desde starter, encontré problemas con las dependencias del entorno virtual local. En concreto, se producían errores al importar pydantic_core y componentes de joblib, por lo que no podía ejecutar correctamente las pruebas ni la inferencia.

### Solución utilizada

Para continuar con el ejercicio, utilicé el entorno virtual de semana3, cuyas dependencias pude importar correctamente.

Trabajé desde el directorio starter, manteniendo activo el entorno de semana3. Para evitar que uv run seleccionara el entorno local de starter, ejecuté los comandos directamente con python -m.

### Comprobaciones realizadas

Desde starter, ejecuté:

```bash
python -m pytest
python -m pytest tests/test_inference_components.py
python -m pytest tests/test_predict_file.py
```

### Resultados obtenidos:

`test_inference_components.py`: 1 test superado.

`test_predict_file.py`: 10 tests superados.

Total: 11 tests superados.

También ejecuté la inferencia local:

```bash
python -m model_inference.predict_file \
  --input assets/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

La ejecución terminó correctamente y generó cinco predicciones en `.tmp/wine_predictions.csv.`
