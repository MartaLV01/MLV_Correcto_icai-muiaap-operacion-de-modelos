# Este es el README para wine-quality-project
(semana02_clase02_assignment.pdf)

Nosotros hemos creado una rama llamada feature/s2-wine-project sobre la que hemos trabajado (paso1)
`git switch -c feature/s2-wine-project`

## Instalacion
Inicializamos proyecto (paso2)
`uv init --package --vcs none --name wine-quality semana2/wine-quality-project`

Comprobamos que estamos en `wine-quality-project` usando: `pwd`y `cd` para omvernos de carpeta
Instalamos las librerias (paso3):
```bash
uv add pandas scikit-learn
uv add --dev pytest ruff #se usa dev para indicar que es para developers
```

## Estructura
Siguiendo lo que nos dicen (paso4).
Creamos las carpetas necesarias con `mkdir`:
```bash
mkdir -p data/raw #-p para que tambien cree las carpetas padre y no error
mkdir -p tests
```

Movemos los archivos
```bash
#cp origen destino

cp ../starter/WineQT.csv data/raw/WineQT.csv
cp ../starter/train.py src/wine_quality/train.py
cp ../starter/test_train.py tests/test_train.py
```

## Comprobaciones
(punto5)

```bash
uv lock #sincronizas librerias del toml en el lock
uv sync --locked #comprueba que el lock y toml son iguales. Sincroniza el venv. Si son distintos da error y no lo cambia.
#uv run python -m wine_quality.train 

#El --frozen evita que se modifique el lock
uv run --frozen python -m wine_quality.train #Ejecuta como modulo (-m)
uv run --frozen pytest
uv run --frozen ruff check .
```

En mi caso el `uv run --frozen pytest`me dio error porque windows no deja acceder al pytest.exe directamente, por ello use:
`$ uv run --frozen python -m pytest`
Lo que hace es cargar el pytest como modulo en python.

## Guardar/Compartir cambios

Al hacer `git status` ves el estado de tus files. 
Si se hace desde algun directorio por debajo del raiz conectado a git aparecera algo como:
``` bash
#si no hay nada por debajo del directorio actual: 
# MLV_Correcto_icai-muiaap-operacion-de-modelos/semana2/wine-quality-project (feature/s2-wine-project)
$ git status
On branch feature/s2-wine-project
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ./

nothing added to commit but untracked files present (use "git add" to track)
```

```bash
#si hay algo debajo del dir actual
# MLV_Correcto_icai-muiaap-operacion-de-modelos/semana2 (feature/s2-wine-project)
$ git status
On branch feature/s2-wine-project
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        wine-quality-project/

nothing added to commit but untracked files present (use "git add" to track)
```

Haciendo, aparece una version abreviada del estado del repo:
```bash
# MLV_Correcto_icai-muiaap-operacion-de-modelos (feature/s2-wine-project)
$ git status --short
?? semana2/wine-quality-project/
```

Hice `cat .gitignore` para ver que no se suba nada que no se deba subir como:
```bash
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.env
```

Despues hice: `git status --short --untracked-files=all` para ver todas las files untrackeadas

hice los commits y el push

