from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---- Contrato del chat con el frontend (YA HECHO, no tocar) ----

# Representa un mensaje de la conversación
class Mensaje(BaseModel):
    # quién ha escrito el mensaje. Solo puede ser "user" o "assistant"
    role: Literal["user", "assistant"]
    content: str # el contenido del mensaje

# lo que recibe nuestro endpoint desde el frontend
# Esel historial de mensajes 
class ChatEntrada(BaseModel):
    mensajes: list[Mensaje] = Field(min_length=1)

# registrar información sobre la herramienta que se ha utilizado
class HerramientaUsada(BaseModel):
    nombre: str
    argumentos: dict
    resultado: dict

# define lo que devolveremos al frontend
class ChatSalida(BaseModel):
    respuesta: str # el texto que recibirá el usuario
    herramienta: Optional[HerramientaUsada] = None
