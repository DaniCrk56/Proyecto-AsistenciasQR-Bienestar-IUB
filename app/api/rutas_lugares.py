from fastapi import APIRouter, HTTPException
from app.models.lugar import Lugar
from app.repositories.lugar_repo import LugarRepository

router = APIRouter(prefix="/lugares", tags=["Gestión de Lugares"])
repo = LugarRepository()

@router.get("/")
def listar_lugares():
    return repo.obtener_todos()

@router.get("/{lugar_id}")
def obtener_lugar(lugar_id: int):
    lugar = repo.obtener_por_id(lugar_id)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar

@router.post("/")
def crear_lugar(lugar: Lugar):
    nuevo_id = repo.crear(lugar)
    return {"mensaje": "Lugar registrado exitosamente", "id": nuevo_id}

@router.delete("/{lugar_id}")
def eliminar_lugar(lugar_id: int):
    exito = repo.eliminar(lugar_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"mensaje": "Lugar eliminado correctamente"}

@router.put("/{lugar_id}")
def actualizar_lugar(lugar_id: int, lugar: Lugar):
    exito = repo.actualizar(lugar_id, lugar)
    if not exito:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"mensaje": "Lugar actualizado correctamente"}