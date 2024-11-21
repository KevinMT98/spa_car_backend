from pydantic import BaseModel, Field
from typing import List, Optional

class GrupoValor(BaseModel):
    id: int
    precio: float

class CategoriaValor(BaseModel):
    categoria: str
    grupos: List[GrupoValor]

class ServicesModel(BaseModel):
    id_servicio: Optional[str] = None
    nombre: str = Field(..., min_length=3, max_length=100)
    tipo_servicio: str = Field(..., min_length=3, max_length=50)
    valores: List[CategoriaValor]

    def to_dict(self):
        return {
            "id_servicio": self.id_servicio,
            "nombre": self.nombre,
            "tipo_servicio": self.tipo_servicio,
            "valores": [
                {
                    "categoria": cat.categoria,
                    "grupos": [
                        {"id": g.id, "precio": str(g.precio)}
                        for g in cat.grupos
                    ]
                }
                for cat in self.valores
            ]
        }

class Servicio:
    def __init__(self, id_servicio: str, nombre: str, tipo_servicio: str):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.tipo_servicio = tipo_servicio
        self.valores = []


__all__ = ['ServicesModel', 'Servicio', 'CategoriaValor', 'GrupoValor']
