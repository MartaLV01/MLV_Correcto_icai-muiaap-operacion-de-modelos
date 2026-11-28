# Solucion
En este archivo contestare a las preguntas de problem/README.md

## M1
1. Anota qué campos aparecen en la primera respuesta y no en la segunda.

En leaky aparece:
```json
    "raw_score": 6.137,
    "threshold_config": "/srv/models/thresholds.yaml"
```
2. Explica en una frase por qué /v1/scores/filtered tampoco los devuelve, aunque la función devuelve un dict con todos ellos.

No los deveuelve ya que se esta indicando con el response_model=PublicScore lo que hay que devolver.

3. En /docs, abre el esquema PublicScore: ¿aparece is_reliable?

Si aparece

## M2
1. Rellena una tabla con status, error.code y error.fields de cada caso.

| peticion | status | error.code | error.fields |
| -------- | ------ | ---------- | ------------ |
| {"age": 30,"income": 1000} | 200 | - | - |
| {"age": "treinta", "income": 1000} | 422 | "validation_error" | {"field":"age","message":"Input should be a valid integer, unable to parse string as an integer"} |
| GET v1/nada | 404 | Not Found | - |
| GET v1/boom | 500 | Internal Server Error| - |

2. ¿Qué devolvería FastAPI en el segundo caso si borraras handle_validation? Pruébalo comentando el decorador y restáuralo después.

Devuelve:
- Code: 422 
- Unprocessable Content
- {"detail":[{"type":"int_parsing","loc":["body","age"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"treinta"}]}

## M3

1. Localiza en /openapi.json dónde terminan summary, el docstring y responses de create_score.

- summary -> Calcular el score de riesgo -> Resumen del endpoint
- description -> Calcula la probabilidad... -> Docstring de create_score
- responses -> Respuestas documentadas -> FastAPI y configuración del endpoint

```json
"summary": "Calcular el score de riesgo",
"description": "Calcula la probabilidad de impago de un cliente.\n\n- `age` entre 18 y 100, `income` mayor que 0.\n- El score es docente: **no** es una decisión de crédito.",
"operationId": "create_score_v1_scores_post",
.....
"responses": {
          "200": {
            "description": "Score y versión del modelo.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ScoringResponse"
                }
              }
            }
          },
          "422": {
            "description": "Entrada fuera de contrato.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ErrorResponse"
                }
              }
            }
          },
          "503": {
            "description": "Modelo no disponible.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ErrorResponse"
                }
              }
            }
          }

```

2. Ejecuta el ejemplo minor desde Swagger con «Try it out».

Code: 422

{"detail":[{"type":"greater_than_equal","loc":["body","age"],"msg":"Input should be greater than or equal to 18","input":16,"ctx":{"ge":18}}]}

3. Añade un tercer ejemplo no_income sin el campo income y comprueba que aparece en el desplegable.

Code: 422

{"detail":[{"type":"missing","loc":["body","income"],"msg":"Field required","input":{"age":30}}]}


Se añadio a openapi_demo.py, la parte del "no income" (actualmente esta comentado):

```json
        Body(
            openapi_examples={
                "valid": {
                    "summary": "Cliente válido",
                    "value": {"age": 42, "income": 38000},
                },
                "minor": {
                    "summary": "Menor de edad: 422",
                    "value": {"age": 16, "income": 1},
                },
                #"no_income": {
                #    "summary": "Sin ingresos",
                #    "value": {
                #        "age": 30
                #    }
                #}
            }
        ),
```

## M4

Con el `"raise_server_exceptions=False"` todos los tests se han ejecutado correctamente.

False -> TestClient permite inspeccionar la respuesta HTTP 500.

Sin el: el test tests/test_examples.py::test_unexpected_error_hides_secrets falla -> RuntimeError: password=TU_SECRETO in /etc/app.conf

Al hacer "response = errors_client.get("/v1/boom")":
1. TestClient envía la petición.
2. FastAPI ejecuta el endpoint /v1/boom.
3. El endpoint lanza RuntimeError.
4. El manejador de excepciones de nuestra aplicación registra el error y prepara la respuesta 500.
5. TestClient vuelve a lanzar la excepción al test.
6. La ejecución se interrumpe y no llegamos a comprobar response.status_code.

True (predeterminado) -> TestClient propaga la excepción al test.