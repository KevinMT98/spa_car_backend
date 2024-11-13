from pydantic import BaseModel, Field, field_validator
from typing import Literal
from decimal import Decimal

class ServicioModel(BaseModel):
    id_servicio: str = Field(..., min_length=1, max_length=10)
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=10, max_length=500)
    precio_base: Decimal = Field(..., gt=0)
    segmento: Literal["Moto", "Auto", "Cuatrimoto"]
    descuento: Decimal = Field(0, ge=0, le=100)  # Porcentaje de descuento
    precio_variable: bool = Field(default=False)  # True si el precio varía según cilindrada
    
    @field_validator("descuento")
    def validar_descuento(cls, v):
        if v < 0 or v > 100:
            raise ValueError("El descuento debe estar entre 0 y 100 por ciento")
        return v
    
    def calcular_precio_final(self, cilindrada: int = 0) -> Decimal:
        precio = self.precio_base
        
        # Ajuste por cilindrada si el precio es variable
        if self.precio_variable and cilindrada > 0:
            if self.segmento == "Moto":
                if cilindrada > 600:
                    precio *= Decimal('1.3')
                elif cilindrada > 300:
                    precio *= Decimal('1.15')
            elif self.segmento in ["Auto", "Cuatrimoto"]:
                if cilindrada > 2000:
                    precio *= Decimal('1.4')
                elif cilindrada > 1600:
                    precio *= Decimal('1.2')
        
        # Aplicar descuento si existe
        if self.descuento > 0:
            precio = precio * (1 - self.descuento / 100)
            
        return precio.quantize(Decimal('0.01'))
    
    def to_dict(self):
        return {
            "id_servicio": self.id_servicio,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio_base": str(self.precio_base),
            "segmento": self.segmento,
            "descuento": str(self.descuento),
            "precio_variable": self.precio_variable
        }

class Servicio:
    def __init__(self, id_servicio: str, nombre: str, descripcion: str, precio_base: Decimal, 
                 segmento: str, descuento: Decimal, precio_variable: bool):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.segmento = segmento
        self.descuento = descuento
        self.precio_variable = precio_variable
    
    def to_dict(self):
        return {
            "id_servicio": self.id_servicio,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio_base": str(self.precio_base),
            "segmento": self.segmento,
            "descuento": str(self.descuento),
            "precio_variable": self.precio_variable
        }
