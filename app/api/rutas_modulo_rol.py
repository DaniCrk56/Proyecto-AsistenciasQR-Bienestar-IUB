from fastapi import APIRouter, HTTPException
from app.models.modulo_rol import ModuloRol
from app.repositories.modulo_rol_repo import ModuloRolRepository

router = APIRouter(prefix="/modulos-roles", tags=["Gestión de Módulos y Roles"])
repo = ModuloRolRepository()

@router.get("/")
def listar_modulos_roles():
    return repo.obtener_todos()

@router.get("/{modulo_rol_id}")
def obtener_modulo_rol(modulo_rol_id: int):
    modulo_rol = repo.obtener_por_id(modulo_rol_id)
    if not modulo_rol:
        raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")
    return modulo_rol

@router.post("/")
def crear_modulo_rol(modulo_rol: ModuloRol):
    nuevo_id = repo.crear(modulo_rol)
    return {"mensaje": "Relación módulo-rol registrada exitosamente", "id": nuevo_id}

@router.delete("/{modulo_rol_id}")
def eliminar_modulo_rol(modulo_rol_id: int):
    exito = repo.eliminar(modulo_rol_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")
    return {"mensaje": "Relación módulo-rol eliminada correctamente"}

@router.put("/{modulo_rol_id}")
def actualizar_modulo_rol(modulo_rol_id: int, modulo_rol: ModuloRol):
    exito = repo.actualizar(modulo_rol_id, modulo_rol)
    if not exito:
        raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")
    return {"mensaje": "Relación módulo-rol actualizada correctamente"}