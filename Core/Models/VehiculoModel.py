from pydantic import BaseModel, Field
from typing import Literal, Optional

class VehiculoModel(BaseModel):
    placa: str = Field(..., min_length=3, max_length=10, alias="Placa")
    documento_cliente: str = Field(..., min_length=3, max_length=10,alias="Documento cliente")
    categoria: Optional[str] = Field (None ,alias="Categoria")
    segmento: Optional[str] = Field (None ,alias="Segmento")
    marca: str = Field(..., min_length=2, max_length=50,alias="Marca")
    linea: Optional[str] = Field (None ,alias="Linea")
    modelo: Optional[str] = Field (None ,alias="Modelo")
    cilindrada: int = Field(..., gt=0,alias="Cilindrada")
    grupo: Optional[str] = Field (None ,alias="Grupo")

    
    def to_dict(self):
        return {
            "Placa": self.placa,
            "Documento cliente": self.documento_cliente,
            "categoria": self.categoria,
            "Segmento": self.segmento,
            "Marca": self.marca,
            "Linea": self.linea,
            "Modelo": self.modelo,
            "Cilindrada": self.cilindrada,
            "Grupo": self.grupo
            }

class Vehiculo:
    def __init__(self, placa, documento_cliente, categoria, segmento,marca,linea, modelo, cilindrada, grupo):
        self.placa = placa
        self.documento_cliente = documento_cliente
        self.categoria = categoria
        self.segmento = segmento
        self.marca = marca
        self.linea = linea
        self.modelo = modelo
        self.cilindrada = cilindrada
        self.grupo = grupo
        
    def to_dict(self):
        return {
            "Placa": self.placa,
            "Documento cliente": self.documento_cliente,
            "categoria": self.categoria,
            "Segmento": self.segmento,
            "Marca": self.marca,
            "Linea": self.linea,
            "Modelo": self.modelo,
            "Cilindrada": self.cilindrada,
            "Grupo": self.grupo
        }
    