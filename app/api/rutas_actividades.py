from fastapi import APIRouter, HTTPException, Depends
from app.api.rutas_auth import validar_administrador
from app.models.actividad import Actividad
from app.repositories.actividad_repo import ActividadRepository

router = APIRouter(prefix="/actividades", tags=["Gestión de Actividades"])
repo = ActividadRepository()

@router.get("/")
def listar_actividades():
    return repo.obtener_todos()

@router.get("/estadisticas/panel")
def obtener_estadisticas(usuario=Depends(validar_administrador)):
    try:
        return repo.obtener_estadisticas()

    except Exception as e:
        print("Error al obtener estadísticas:", e)
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener las estadísticas"
        )

@router.get("/{actividad_id}")
def obtener_actividad(actividad_id: int):
    actividad = repo.obtener_por_id(actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad

@router.post("/")
def crear_actividad(actividad: Actividad):
    nuevo_id = repo.crear(actividad)
    return {"mensaje": "Actividad registrada exitosamente", "id": nuevo_id}

@router.delete("/{actividad_id}")
def eliminar_actividad(actividad_id: int):
    exito = repo.eliminar(actividad_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return {"mensaje": "Actividad eliminada correctamente"}

@router.put("/{actividad_id}")
def actualizar_actividad(actividad_id: int, actividad: Actividad):
    exito = repo.actualizar(actividad_id, actividad)
    if not exito:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return {"mensaje": "Actividad actualizada correctamente"}
