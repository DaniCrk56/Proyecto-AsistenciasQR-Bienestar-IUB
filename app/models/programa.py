from pydantic import BaseModel
from typing import Optional

class Programa(BaseModel):
    id: Optional[int] = None
    nombre: str
    codigo: str
    estado: bool = True