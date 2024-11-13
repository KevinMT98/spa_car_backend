from pydantic import BaseModel, Field
from typing import Literal, Optional

class VehiculoModel(BaseModel):
    placa: str = Field(..., min_length=3, max_length=10, alias="Placa")
    documento_cliente: str = Field(..., min_length=3, max_length=10,alias="Documento cliente")
    segmento: Literal["Moto", "Auto", "Cuatrimoto"] = Field(..., min_length=2, max_length=50,alias="Segmento")
    marca: str = Field(..., min_length=2, max_length=50,alias="Marca")
    linea: Optional[str] = Field (None ,alias="Linea")
    modelo: Optional[str] = Field (None ,alias="Modelo")
    cilindrada: int = Field(..., gt=0,alias="Cilindrada")
    tipo: Literal["Sport", "Naked", "Camioneta", 
                  "Automóvil", "Touring", "Otro," 
                  "No aplica"] = Field(..., min_length=2, max_length=50,alias="Tipo")
    
    def to_dict(self):
        return {
            "Placa": self.placa,
            "Documento cliente": self.documento_cliente,
            "Segmento": self.segmento,
            "Marca": self.marca,
            "Linea": self.linea,
            "Modelo": self.modelo,
            "Cilindrada": self.cilindrada,
            "Tipo": self.tipo
            }

class Vehiculo:
    def __init__(self, placa, documento_cliente, segmento, marca,linea, modelo, cilindrada, tipo):
        self.placa = placa
        self.documento_cliente = documento_cliente
        self.segmento = segmento
        self.marca = marca
        self.linea = linea
        self.modelo = modelo
        self.cilindrada = cilindrada
        self.tipo = tipo
        
    def to_dict(self):
        return {
            "Placa": self.placa,
            "Documento cliente": self.documento_cliente,
            "Segmento": self.segmento,
            "Marca": self.marca,
            "Linea": self.linea,
            "Modelo": self.modelo,
            "Cilindrada": self.cilindrada,
            "Tipo": self.tipo
        }
    