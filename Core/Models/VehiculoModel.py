from pydantic import BaseModel, Field
from typing import Literal#

class VehiculoModel(BaseModel):
    id_vehiculo: str = Field(..., min_length=3, max_length=10, alias="placa")
    cedula_cliente: str = Field(..., min_length=3, max_length=10)
    tipo_vehiculo: Literal["Moto", "Auto", "Cuatrimoto"]
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    cilindrada: int = Field(..., gt=0)
    tipo: Literal["Sport", "Naked", "Camioneta", "Automóvil", "Touring", "Otro"]
    
    def to_dict(self):
        return {
            "id_vehiculo": self.id_vehiculo,
            "cedula_cliente": self.cedula_cliente,
            "tipo_vehiculo": self.tipo_vehiculo,
            "marca": self.marca,
            "modelo": self.modelo,
            "cilindrada": self.cilindrada,
            "tipo": self.tipo
            }

class Vehiculo:
    def __init__(self, id_vehiculo, cedula_cliente, tipo_vehiculo, marca, modelo, cilindrada, tipo):
        self.id_vehiculo = id_vehiculo
        self.cedula_cliente = cedula_cliente
        self.tipo_vehiculo = tipo_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.cilindrada = cilindrada
        self.tipo = tipo
        
    def to_dict(self):
        return {
            "id_vehiculo": self.id_vehiculo,
            "cedula_cliente": self.cedula_cliente,
            "tipo_vehiculo": self.tipo_vehiculo,
            "marca": self.marca,
            "modelo": self.modelo,
            "cilindrada": self.cilindrada,
            "tipo": self.tipo
        }
    