En este archivo escribire los resultados de los print que vaya ejecutando en aemet_api.py
Inlcuyendo mis comentarios para entener que esta pasando

```python
print(response.status_code)
print(response.text)
```

```text
200
{
  "descripcion" : "exito",
  "estado" : 200,
  "datos" : "https://opendata.aemet.es/opendata/sh/e70b0ce6",
  "metadatos" : "https://opendata.aemet.es/opendata/sh/0556af7a"
}
```
**Primer print:**
200: la petición HTTP se ha realizado correctamente

**Segundo print:**

"estado": 200: AEMET confirma que la solicitud ha tenido éxito.

"datos": contiene la URL desde la que podemos descargar el inventario de estaciones.

"metadatos": contiene información sobre la estructura de los datos.

```python
print("\n", estaciones) #imprime todas la estaciones. NO es lo que queremos
```
Esta es la ultima entrada:
```text
..., {'latitud': '405517N', 'provincia': 'TERUEL', 'altitud': '1006', 'indicativo': '9998X', 'nombre': 'BELLO', 'indsinop': '', 'longitud': '012940W'}]
```


```python
print("Indicativo: ", idema)
print("Estacion Madrid, Cuidad Universitaria: \n", estacion)
```

Imprime en consola:
```text
Indicativo: 3194U
Estacion Madrid, Cuidad Universitaria: 
 {'latitud': '402706N', 'provincia': 'MADRID', 'altitud': '664', 'indicativo': '3194U', 'nombre': 'MADRID, CIUDAD UNIVERSITARIA', 'indsinop': '08220', 'longitud': '034327W'}
```

```python
print("\nCLIMATOLOGIA DIARIA:")
print("Status code: ", response_clima_diario.status_code) #vemos el status d enuestra peticion. Deberia ser 200
print("Informacion:\n", response_clima_diario.text) #imprime la info de nuestra peticion
```

```text
CLIMATOLOGIA DIARIA:
Status code:  200
Informacion:
 {
  "descripcion" : "exito",
  "estado" : 200,
  "datos" : "https://opendata.aemet.es/opendata/sh/f01f0236",
  "metadatos" : "https://opendata.aemet.es/opendata/sh/b3aa9d28"
}
```

status_code = 200: la petición HTTP se ha procesado correctamente.

"estado": 200: AEMET confirma que la consulta ha tenido éxito.

"datos": la URL desde la que puedes descargar los registros climatológicos.

"metadatos": información sobre la estructura de los datos.

```python
print("\nCLIMA DIARIO: \n", clima_diario)

print("\n", type(clima_diario))       # Tipo de objeto
print(len(clima_diario))        # Número de registros diarios
print(clima_diario[0].keys())   # Campos disponibles
```

Esta es la ultima entrada:
```text
..., {'fecha': '2019-10-30', 'indicativo': '3194U', 'nombre': 'MADRID, CIUDAD UNIVERSITARIA', 'provincia': 'MADRID', 'altitud': '664', 'tmed': '13,7', 'prec': '0,0', 'tmin': '9,0', 'horatmin': '07:00', 'tmax': '18,4', 'horatmax': '13:40', 'hrMedia': '63', 'hrMax': '86', 'horaHrMax': 'Varias', 'hrMin': '50', 'horaHrMin': '14:00', 'pintMax': '0,0'}]

 <class 'list'>
30
dict_keys(['fecha', 'indicativo', 'nombre', 'provincia', 'altitud', 'tmed', 'prec', 'tmin', 'horatmin', 'tmax', 'horatmax', 'hrMedia', 'hrMax', 'horaHrMax', 'hrMin', 'horaHrMin', 'pintMax'])
```