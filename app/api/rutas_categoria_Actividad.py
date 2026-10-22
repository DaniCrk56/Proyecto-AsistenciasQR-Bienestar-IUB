from fastapi import APIRouter, HTTPException
from app.models.categoria_actividad import CategoriaActividad
from app.repositories.categoria_actividad_repo import CategoriaActividadRepository

router = APIRouter(prefix="/categorias-actividad", tags=["Gestión de Categorías de Actividad"])
repo = CategoriaActividadRepository()

@router.get("/")
def listar_categorias():
    return repo.obtener_todos()

@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    categoria = repo.obtener_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/")
def crear_categoria(categoria: CategoriaActividad):
    nuevo_id = repo.crear(categoria)
    return {"mensaje": "Categoría registrada exitosamente", "id": nuevo_id}

@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    exito = repo.eliminar(categoria_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría eliminada correctamente"}

@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, categoria: CategoriaActividad):
    exito = repo.actualizar(categoria_id, categoria)
    if not exito:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría actualizada correctamente"}