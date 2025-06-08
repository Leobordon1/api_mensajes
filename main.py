from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

# Modelo del mensaje
class Mensaje(BaseModel):
    id: Optional[int] = None
    user: str
    mensaje: str

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Base de datos simulada (lista en memoria)
mensajes_db: List[Mensaje] = []

@app.post("/mensajes", response_model=Mensaje)
def crear_mensaje(mensaje: Mensaje):
    mensaje.id = len(mensajes_db) + 1
    mensajes_db.append(mensaje)
    return mensaje
