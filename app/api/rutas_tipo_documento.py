from fastapi import APIRouter, HTTPException
from app.models.tipo_documento import TipoDocumento
from app.repositories.tipo_documento_repo import TipoDocumentoRepository

router = APIRouter(prefix="/tipos-documento", tags=["Gestión de Tipos de Documento"])
repo = TipoDocumentoRepository()

@router.get("/")
def listar_tipos_documento():
    return repo.obtener_todos()

@router.get("/{tipo_doc_id}")
def obtener_tipo_documento(tipo_doc_id: int):
    tipo_doc = repo.obtener_por_id(tipo_doc_id)
    if not tipo_doc:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_doc

@router.post("/")
def crear_tipo_documento(tipo_doc: TipoDocumento):
    nuevo_id = repo.crear(tipo_doc)
    return {"mensaje": "Tipo de documento registrado exitosamente", "id": nuevo_id}

@router.delete("/{tipo_doc_id}")
def eliminar_tipo_documento(tipo_doc_id: int):
    exito = repo.eliminar(tipo_doc_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return {"mensaje": "Tipo de documento eliminado correctamente"}

@router.put("/{tipo_doc_id}")
def actualizar_tipo_documento(tipo_doc_id: int, tipo_doc: TipoDocumento):
    exito = repo.actualizar(tipo_doc_id, tipo_doc)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return {"mensaje": "Tipo de documento actualizado correctamente"}