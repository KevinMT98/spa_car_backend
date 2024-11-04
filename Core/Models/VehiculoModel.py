from pydantic import BaseModel, Field
from typing import Literal

class VehiculoModel(BaseModel):
    id_vehiculo: str = Field(..., min_length=3, max_length=10, alias="placa")
    tipo_vehiculo: Literal["Moto", "Auto", "Cuatrimoto"]
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    cilindrada: int = Field(..., gt=0)
    tipo: Literal["Sport", "Naked", "Camioneta", "Automóvil", "Touring", "Otro"]
    cedula_cliente: str = Field(..., min_length=3, max_length=10)