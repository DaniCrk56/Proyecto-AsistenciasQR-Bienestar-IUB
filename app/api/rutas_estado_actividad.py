from fastapi import APIRouter, HTTPException
from app.models.estado_actividad import EstadoActividad
from app.repositories.estado_actividad_repo import EstadoActividadRepository

router = APIRouter(prefix="/estados-actividad", tags=["Gestión de Estados de Actividad"])
repo = EstadoActividadRepository()

@router.get("/")
def listar_estados():
    return repo.obtener_todos()

@router.get("/{estado_id}")
def obtener_estado(estado_id: int):
    estado = repo.obtener_por_id(estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.post("/")
def crear_estado(estado: EstadoActividad):
    nuevo_id = repo.crear(estado)
    return {"mensaje": "Estado registrado exitosamente", "id": nuevo_id}

@router.delete("/{estado_id}")
def eliminar_estado(estado_id: int):
    exito = repo.eliminar(estado_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return {"mensaje": "Estado eliminado correctamente"}

@router.put("/{estado_id}")
def actualizar_estado(estado_id: int, estado: EstadoActividad):
    exito = repo.actualizar(estado_id, estado)
    if not exito:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return {"mensaje": "Estado actualizado correctamente"}