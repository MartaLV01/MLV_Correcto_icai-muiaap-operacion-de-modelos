"""
Usando la librería de Python requests , llama a la API de la AEMET para obtener la climatología diaria durante 
el mes de octubre de 2019 en la Ciudad Universitaria de Madrid.
"""
import requests

requests.get(
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones",
    headers={
      "api_key": "YOUR_SECRET_TOKEN"
    }
)