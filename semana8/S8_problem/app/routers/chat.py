from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


# DONE -> TODO: POST /chat (entrada ChatEntrada, salida ChatSalida). Recibe el LLM con Depends(get_llm)
# con el decorador decimos que la funcion responde a 
# peticiones d etipo POST
# en la ruta /chat
# al hacer response_model=ChatSalida se le indica que 
# la respuesta debe ajustarse al modelo ChatSalida
# entrada: ChatEntrada -> FastAPI interpreta que debe 
# recibir el JSON del frontend y validarlo utilizando ChatEntrada
@router.post("/chat", response_model=ChatSalida)
# antes de llamar a la funcion obtiene el llm que se usara
# por defecto es un llm simulado
# se guarda en llm
# get_llm -> nos da el llm por defecto es el simulado
# se podrai usar dentro de la funcion -> llm = get_llm
# pero con depends se puden hacer test con falsos llms
def chat(entrada: ChatEntrada, llm=Depends(get_llm)):
    return responder(entrada.mensajes, llm)
