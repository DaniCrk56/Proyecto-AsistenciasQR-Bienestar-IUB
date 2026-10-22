from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Actividad(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    lugar_id: int
    categoria_id: int
    estado_id: int
    estado: bool = True