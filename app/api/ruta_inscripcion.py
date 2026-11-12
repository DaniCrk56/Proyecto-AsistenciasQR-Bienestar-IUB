
from fastapi import APIRouter, HTTPException
from app.models.inscripcion import Inscripcion
from app.repositories.inscripcion_repo import InscripcionRepository

router = APIRouter(prefix="/inscripciones", tags=["Gestión de Inscripciones"])
repo = InscripcionRepository()


@router.get("/")
def listar_inscripciones():
    return repo.obtener_todos()


@router.get("/estudiante/{usuario_id}")
def listar_inscripciones_estudiante(usuario_id: int):
    inscripciones = repo.obtener_por_estudiante(usuario_id)

    return inscripciones


@router.get("/{inscripcion_id}")
def obtener_inscripcion(inscripcion_id: int):
    inscripcion = repo.obtener_por_id(inscripcion_id)

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    return inscripcion


@router.post("/")
def crear_inscripcion(inscripcion: Inscripcion):
    resultado = repo.crear(inscripcion)

    if resultado is None:
        raise HTTPException(
            status_code=500,
            detail="No fue posible conectar con la base de datos"
        )

    if resultado == "duplicada":
        raise HTTPException(
            status_code=409,
            detail="Ya estás inscrito en este evento"
        )

    return {
        "mensaje": "Inscripción registrada exitosamente",
        "id": resultado["id"],
        "codigo_qr": str(resultado["codigo_qr"])
    }


@router.delete("/{inscripcion_id}")
def eliminar_inscripcion(inscripcion_id: int):
    exito = repo.eliminar(inscripcion_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    return {"mensaje": "Inscripción eliminada correctamente"}


@router.put("/{inscripcion_id}")
def actualizar_inscripcion(inscripcion_id: int, inscripcion: Inscripcion):
    exito = repo.actualizar(inscripcion_id, inscripcion)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    return {"mensaje": "Inscripción actualizada correctamente"}
