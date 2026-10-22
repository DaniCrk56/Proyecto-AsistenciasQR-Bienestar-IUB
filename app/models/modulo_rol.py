from pydantic import BaseModel
from typing import Optional

class ModuloRol(BaseModel):
    id: Optional[int] = None
    modulo_id: int
    rol_id: int
    estado: bool = True