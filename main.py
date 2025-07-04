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

# Ruta de bienvenida
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de mensajes de Leo",
        "endpoints_disponibles": [
            "GET /mensajes",
            "GET /mensajes/{id}",
            "POST /mensajes",
            "PUT /mensajes/{id}",
            "DELETE /mensajes/{id}"
        ]
    }

@app.post("/mensajes", response_model=Mensaje)
def crear_mensaje(mensaje: Mensaje):
    mensaje.id = len(mensajes_db) + 1
    mensajes_db.append(mensaje)
    return mensaje

# Obtener un mensaje por su ID
@app.get("/mensajes/{mensaje_id}", response_model=Mensaje)
def obtener_mensaje(mensaje_id: int):
    for mensaje in mensajes_db:
        if mensaje.id == mensaje_id:
            return mensaje
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")

# Listar todos los mensajes
@app.get("/mensajes", response_model=List[Mensaje])
def listar_mensajes():
    return mensajes_db

# Actualizar un mensaje existente
@app.put("/mensajes/{mensaje_id}", response_model=Mensaje)
def actualizar_mensaje(mensaje_id: int, mensaje_actualizado: Mensaje):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            mensaje_actualizado.id = mensaje_id
            mensajes_db[index] = mensaje_actualizado
            return mensaje_actualizado
    raise HTTPException(status_code=404, detail="Mensaje no encontrado para actualizar")

# Eliminar un mensaje por su ID
@app.delete("/mensajes/{mensaje_id}", response_model=dict)
def eliminar_mensaje(mensaje_id: int):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            del mensajes_db[index]
            return {"detail": "Mensaje eliminado"}
    raise HTTPException(status_code=404, detail="Mensaje no encontrado para eliminar")
