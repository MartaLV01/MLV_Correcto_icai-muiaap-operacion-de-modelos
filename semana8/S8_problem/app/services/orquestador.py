import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# DONE -> TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
# construir la definición de una herramienta para que el LLM sepa que puede utilizarla
def definir_tool() -> dict:
    return {
        # Se le dice a la API del LLM que esta herramienta 
        # es una función que puede invocar
        "type": "function", 
        # se define la funcion
        "function": {
            "name": NOMBRE_TOOL, # nombre que el LLM utilizará cuando quiera solicitar su ejecución
            # Es una descripción en lenguaje natural
            # Sirve para que el LLM entienda cuándo debe utilizar la herramienta
            "description": (
                "Calcula la probabilidad de impago de una solicitud de préstamo "
                "y devuelve si es aceptada, rechazada o necesita revision."
            ),
            "parameters": PrestamoEntrada.model_json_schema(),
            # con model_json_schema se genera automáticamente el esquema JSON a partir 
            # de tu modelo Pydantic (PrestamoEntrada) asi no hay que escribirlo de nuevo
        },
    }

# DONE -> TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error -> {"ok": False, "error": "..."})
def ejecutar_tool(nombre, argumentos_json) -> dict:
    # Comprobar que la herramienta existe
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": f"Herramienta desconocida: {nombre}"}

    # Convertir el JSON en un diccionario
    try:
        datos = json.loads(argumentos_json) # pasa el json a diccionario python
        if not isinstance(datos, dict):
            return {"ok": False, "error": "Los argumentos deben ser un objeto JSON."}
    
        # Validar los datos con Pydantic -> entrada sera un objeto PrestamoEntrada
        entrada = PrestamoEntrada.model_validate(datos)
    
        # Ejecutar la predicción
        salida = predecir(entrada) # (services/modelo.py)
        return {"ok": True, **salida.model_dump()}
        # salida.model_dump() pasa el objeto pydantic a diccionario
        # con ** se desempaqueta el diccionario
        # de esta manera se podra devolver:
        #{
        #    "ok": True,
        #    "probabilidad_impago": 0.12,
        #    "decision": "aprobar"
        #}
    
    except (json.JSONDecodeError, TypeError) as error:
            return {"ok": False, "error": f"Los argumentos no contienen un JSON válido: {error}"}

    except ValidationError as error:
            return {"ok": False, "error": str(error)}

    except Exception as error:
        return {"ok": False, "error": str(error)}
    
# DONE -> TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)

# coordinar toda la conversación
def responder(mensajes, llm) -> ChatSalida:
    # Preparamos el historial de conversación
    # System contiene las instrucciones generales del asistente
    # system sera el primer "mensaje"
    historial = [{"role": "system", "content": SISTEMA}]

    # se usa dump para pasar a disccionario el obejto Pydantic (mensaje)
    # con extend se añade el contenido de una lista/coleccion dentro de otra lista
    # como objetos independientes y no en conjunto (como hace el append)
    # numeros = [1, 2, 3] -> numeros.append([4, 5]) -> [1, 2, 3, [4, 5]]
    # numeros = [1, 2, 3] -> numeros.extend([4, 5]) -> [1, 2, 3, 4, 5]
    # tambien s epodria usar append si antes recorrieramos todos los mensajes con un for:
    # for m in mensajes:
    #     historial.append(m.model_dump())
    historial.extend([m.model_dump() for m in mensajes])

    # none ya que en un principio no es necesario usar un modelo
    # dependera de lo que el user pregunte
    herramienta_usada = None

    # Consultamos al LLM como máximo MAX_VUELTAS veces
    #_ -> por que no necesitamos conocer el numeor de iteracion
    # se hacen la itrarciones como max el MAX_VUELTAS
    for _ in range(MAX_VUELTAS):

        # comunicacion conn el llm -> historial y tool
        # entre [] porque es una lista
        mensaje = llm.completar(historial, [definir_tool()])

        # Comprobamos si el LLM solicita una herramienta
        tool_calls = mensaje.get("tool_calls")

        # si el asistente necesita mas datos del user se lo spide
        # para ello no es necesario llamar a un modelo
        # como el asistente ha respondido se sale del bucle
        # {"role": "assistant", "content": "Me faltan algunos datos..."}
        if not tool_calls:
            return ChatSalida(
                respuesta=mensaje.get("content") or "",
                herramienta=herramienta_usada
            )

        # si el asistente tiene la info se continua:
        # Ejemplo: {"role": "assistant", "content": None, "tool_calls": [...]}

        # Añadimos al historial el mensaje del asistente
        historial.append(mensaje)

        # Ejecutamos la herramienta solicitada
        # accedemos a la primera herramienta solicitada
        # en este caso es: nombre = "calcular_riesgo_impago"
        llamada = tool_calls[0] 

        nombre = llamada["function"]["name"]
        argumentos_json = llamada["function"]["arguments"]

        # s eejecuta la herramineta
        resultado = ejecutar_tool(nombre, argumentos_json)

        # Guardamos la información de la herramienta utilizada
        # schemas/chat.py
        herramienta_usada = HerramientaUsada(
            nombre=nombre,
            argumentos=leer_argumentos(argumentos_json),
            resultado=resultado
        )

        # Devolvemos el resultado al LLM como mensaje tool
        # con el dump pasamos de python a JSON
        historial.append({
            "role": "tool",
            "tool_call_id": llamada["id"],
            "content": json.dumps(resultado)
        })

        # continua con la siguiente iteracion del bucle
        # pero como lo hemos definido como tool
        # tool_calls esta vacio y sale del bucle

    # 8. Si agotamos las vueltas, devolvemos un mensaje de seguridad
    return ChatSalida(
        respuesta="No he podido completar la operación dentro del límite de intentos.",
        herramienta=herramienta_usada
    )    