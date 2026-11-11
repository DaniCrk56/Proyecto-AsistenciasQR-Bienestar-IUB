
from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class Actividad(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int
    id_lugar: int
    id_categoria: int
    id_estado_actividad: int
    id_responsable: Optional[int] = None
    estado: bool = True
