from fastapi import APIRouter, HTTPException
from app.models.inscripcion import Inscripcion
from app.repositories.inscripcion_repo import InscripcionRepository

router = APIRouter(prefix="/inscripciones", tags=["Gestión de Inscripciones"])
repo = InscripcionRepository()

@router.get("/")
def listar_inscripciones():
    return repo.obtener_todos()

@router.get("/{inscripcion_id}")
def obtener_inscripcion(inscripcion_id: int):
    inscripcion = repo.obtener_por_id(inscripcion_id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return inscripcion

@router.post("/")
def crear_inscripcion(inscripcion: Inscripcion):
    nuevo_id = repo.crear(inscripcion)
    return {"mensaje": "Inscripción registrada exitosamente", "id": nuevo_id}

@router.delete("/{inscripcion_id}")
def eliminar_inscripcion(inscripcion_id: int):
    exito = repo.eliminar(inscripcion_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Inscripción eliminada correctamente"}

@router.put("/{inscripcion_id}")
def actualizar_inscripcion(inscripcion_id: int, inscripcion: Inscripcion):
    exito = repo.actualizar(inscripcion_id, inscripcion)
    if not exito:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Inscripción actualizada correctamente"}