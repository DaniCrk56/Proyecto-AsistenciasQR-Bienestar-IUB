from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.models.asistencia import Asistencia
from app.repositories.asistencia_repo import AsistenciaRepository
from app.api.rutas_auth import validar_administrador

router = APIRouter(prefix="/asistencias", tags=["Gestión de Asistencias"])
repo = AsistenciaRepository()

class DatosEscaneoQR(BaseModel):
    codigo_qr: str
    id_evento: int

@router.get("/")
def listar_asistencias():
    return repo.obtener_todos()
    
    @router.get("/evento/{id_evento}")
def listar_asistencias_evento(
    id_evento: int,
    administrador: dict = Depends(validar_administrador)
):
    return repo.obtener_por_evento(id_evento)

@router.get("/{asistencia_id}")
def obtener_asistencia(asistencia_id: int):
    asistencia = repo.obtener_por_id(asistencia_id)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return asistencia

@router.post("/")
def crear_asistencia(asistencia: Asistencia):
    nuevo_id = repo.crear(asistencia)
    return {"mensaje": "Asistencia registrada exitosamente", "id": nuevo_id}

@router.delete("/{asistencia_id}")
def eliminar_asistencia(asistencia_id: int):
    exito = repo.eliminar(asistencia_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return {"mensaje": "Asistencia eliminada correctamente"}

@router.put("/{asistencia_id}")
def actualizar_asistencia(asistencia_id: int, asistencia: Asistencia):
    exito = repo.actualizar(asistencia_id, asistencia)
    if not exito:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return {"mensaje": "Asistencia actualizada correctamente"}

@router.post("/escanear")
def escanear_qr(
    datos: DatosEscaneoQR,
    administrador: dict = Depends(validar_administrador)
):

    resultado = repo.registrar_por_qr(
        datos.codigo_qr,
        datos.id_evento,
        administrador["usuario_id"]
    )

    if resultado["estado"] == "no_encontrada":
        raise HTTPException(
            status_code=404,
            detail="QR inválido o no pertenece a este evento"
        )

    if resultado["estado"] == "duplicada":
        raise HTTPException(
            status_code=409,
            detail="Este estudiante ya tiene asistencia registrada"
        )

    if resultado["estado"] == "error":
        raise HTTPException(
            status_code=500,
            detail="No se pudo conectar con la base de datos"
        )

    return {
        "mensaje": "Asistencia registrada exitosamente",
        "id": resultado["id"]
    }
