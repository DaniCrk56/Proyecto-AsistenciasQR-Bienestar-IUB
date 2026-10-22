from pydantic import BaseModel
from typing import Optional

class Asistencia(BaseModel):
    id: Optional[int] = None
    inscripcion_id: int
    asistio: bool = True
    estado: bool = True