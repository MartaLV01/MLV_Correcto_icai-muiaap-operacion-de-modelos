Distintos ejemplos para ver el funcionamineto de la libreria streamlit

Se usa el controlador de entornos uv (solo hay que hacer `uv sync` por que el .toml y el .lock estan compartidos)

El archivo .ipynb hace lo mismo que cada uno de los archivos .py de `scripts/`

He completado los TODOs de `05_practica_starter.py`

Para ejecutar se usa el comando: uv run streamlit run nombre_del_archivo.py (para mas informacion ver el archivo `scripts/README_scripts.txt`)

`tests/test_miercoles` contiene varios tests para las 5 files.py de `scripts/` (excluyendo `modelo.py`)

Se ejecutan todos al hacer en la terminal `uv run pytest`

Pasan: 
1. `test_contador_roto_no_recuerda`
2. `test_contador_con_estado_y_callback`
3. `test_app_ejemplo_historial`

Fallan:
1. El test `test_starter_arranca_y_esta_incompleto` falla porque comprueba en `05_practica_starter.py` que el starter arranca y que todavía no se ha inicializado history
2. `test_starter_con_huecos_resueltos_funciona` falla porque mira por expresiones especificas que yo he cmabiado al hacer los TODOs, no porque el codigo este mal.