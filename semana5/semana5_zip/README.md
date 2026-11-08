Distintos ejemplos para ver el funcionamineto de la libreria streamlit

Se usa el controlador de entornos uv (solo hay que hacer `uv sync` por que el `.toml`y el `.lock` estan compartidos)

El archivo .ipynb crea los archivos `app_xx.py` y la carpeta y archivos de `demo_stremlit`

Por mi parte he creado los tres archivos `mi_web_`:
1. `mi_web.py` crea un CV statico (los datos son inventados)
2. `mi_web_CV_desplegable.py` crea un CV con datos staticos pero que cada apartado es desplegable (los datos son inventados)
3. `mi_web_recomendador_libros.py` es un recoemndador de libros interactivo.

Para ejecutar se usa el comando:
`uv run streamlit run nombre_del_archivo.py`