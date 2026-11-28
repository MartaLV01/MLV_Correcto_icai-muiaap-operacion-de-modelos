Como hice los ejercicios fuera de este repositorio y para la entrega he copiado solo los de los ejercicios, la carpeta de ejemplos al hacer los ejercicios de la carpeta `01-api.microexercises/` no va a poder ejecutarse con el comando `uv run fastapi dev examples/serialization_demo.py` desde esta carpeta. 

Para ejecutarse hay que cambiar la doreccion: 
- `uv run fastapi dev modules/09-api-professional/examples/`+ nombre del archivo

Por ejemplo:  `uv run fastapi dev modules/09-api-professional/examples/serialization_demo.py`

El environment usado ha sido el de `semana9\pyproject.toml` es el mismo que el de `semana9\modules\09-api-professional\pyproject.toml`