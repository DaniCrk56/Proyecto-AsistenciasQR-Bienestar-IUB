from pydantic import BaseModel
from typing import Optional

class Inscripcion(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    actividad_id: int
    estado: bool = True