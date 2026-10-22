from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    tipo_documento_id: int
    numero_documento: str
    nombre: str
    apellido: str
    email: str
    password: str
    rol_id: int
    estado: bool = True