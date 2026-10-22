from pydantic import BaseModel
from typing import Optional

class Lugar(BaseModel):
    id: Optional[int] = None
    nombre: str
    capacidad: int
    ubicacion: Optional[str] = None
    estado: bool = True