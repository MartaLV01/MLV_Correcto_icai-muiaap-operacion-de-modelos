"""
En aemet_api_resultados.md ire escribiendo la salida de los diversos prints y escribiendo notas sobre ellos.

ENUNCIADO:
Usando la librería de Python requests , llama a la API de la AEMET para obtener la climatología diaria durante 
el mes de octubre de 2019 en la Ciudad Universitaria de Madrid.
"""

"""
En la web: https://opendata.aemet.es/dist/index.html#tag/valores-climatologicos/GET/api/valores/climatologicos/inventarioestaciones/estaciones/{estaciones}
La api key se pasa como header:
requests.get(
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones",
    headers={
      "api_key": "YOUR_SECRET_TOKEN"
    }
)
Pero no es lo que queremos, el enunciado dice que sea como parametro -> params:
"""

import os
from dotenv import load_dotenv
import requests


url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

#api_key = AEMET_API_KEY

load_dotenv() # carga las variables del archivo .env en el entorno del proceso

api_key = os.getenv("AEMET_API_KEY") # recupera el valor de AEMET_API_KEY

if not api_key:
    raise ValueError("No se ha encontrado la API key de AEMET")

response = requests.get(
    url,
    params={"api_key": api_key}
)

print("Status code: ", response.status_code) #vemos el status d enuestra peticion. Deberia ser 200
print("Informacion: \n", response.text) #imprime la info de nuestra peticion

# nos interesa la url del inventario. Del print (print(response.text)) hemos sacado que se encuetra en "datos"
# tambien lo podemos hacer con: response.json().keys() 
#   en donde vemos todas la keys del json devuelto
url_datos = response.json()["datos"] 

response_datos = requests.get(url_datos) #obtenemos el contenido de la url
response_datos.raise_for_status() #vemos el estado y si es mayor igual a 400 salta el error

estaciones = response_datos.json() #la info del json la paso a objeto python

#print("\n", estaciones) #imprime todas la estaciones. NO es lo que queremos

for estacion in estaciones:
    if estacion.get("nombre", "").upper() == "MADRID, CIUDAD UNIVERSITARIA":
      idema = estacion["indicativo"]
      print("\nIndicativo: ", idema)
      print("Estacion Madrid, Cuidad Universitaria: \n", estacion)

#paso 3 -> llamar a climatilogias diarias:
"""
Lo que viene en la pagina web de aemet
requests.get(
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{idema}",
    headers={
      "api_key": "YOUR_SECRET_TOKEN"
    }
)
"""

fechaIniStr = "2019-10-01T00:00:00UTC"
fechaFinStr = "2019-10-30T23:59:59UTC"
idema = "3194U"

url_clima_diario = (
    f"https://opendata.aemet.es/opendata/api/valores/climatologicos/"
    f"diarios/datos/fechaini/{fechaIniStr}/"
    f"fechafin/{fechaFinStr}/estacion/{idema}"
)
response_clima_diario = requests.get(
    url_clima_diario,
    params={"api_key": api_key}
)
print("\nCLIMATOLOGIA DIARIA:")
print("Status code: ", response_clima_diario.status_code) #vemos el status d enuestra peticion. Deberia ser 200
print("Informacion:\n", response_clima_diario.text) #imprime la info de nuestra peticion

url_datos_clima = response_clima_diario.json()["datos"]

response_datos_clima = requests.get(url_datos_clima)
response_datos_clima.raise_for_status()

clima_diario = response_datos_clima.json()

print("\nCLIMA DIARIO: \n", clima_diario)

print("\n", type(clima_diario))       # Tipo de objeto
print(len(clima_diario))        # Número de registros diarios
print(clima_diario[0].keys())   # Campos disponibles