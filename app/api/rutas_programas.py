from fastapi import APIRouter, HTTPException
from app.models.programa import Programa
from app.repositories.programa_repo import ProgramaRepository

router = APIRouter(prefix="/programas", tags=["Gestión de Programas"])
repo = ProgramaRepository()

@router.get("/")
def listar_programas():
    return repo.obtener_todos()

@router.get("/{programa_id}")
def obtener_programa(programa_id: int):
    programa = repo.obtener_por_id(programa_id)
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa

@router.post("/")
def crear_programa(programa: Programa):
    nuevo_id = repo.crear(programa)
    return {"mensaje": "Programa registrado exitosamente", "id": nuevo_id}

@router.delete("/{programa_id}")
def eliminar_programa(programa_id: int):
    exito = repo.eliminar(programa_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return {"mensaje": "Programa eliminado correctamente"}

@router.put("/{programa_id}")
def actualizar_programa(programa_id: int, programa: Programa):
    exito = repo.actualizar(programa_id, programa)
    if not exito:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return {"mensaje": "Programa actualizado correctamente"}