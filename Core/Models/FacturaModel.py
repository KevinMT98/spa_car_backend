from typing import List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional


class ServicioFactura(BaseModel):
    id_servicio: int = Field(alias='servicio', default= 9999)
    cantidad: Optional[int] = 1
    descripcion: str
    valor: float

    @field_validator('id_servicio')
    def validate_id_servicio(cls, v):
        if not v:
            return 9999
        return v

class Factura(BaseModel):
    numero_factura: Optional[int] = None
    fecha: datetime
    placa: str
    categoria: str
    grupo: int
    id_cliente: str 
    medio_pago: str
    descuento: float = Field(default=0.0)
    vlr_descuento: float = Field(default=0.0)
    subtotal: float = Field(default=0.0)
    total: float = Field(default=0.0)
    servicios: List[ServicioFactura]

    @field_validator('numero_factura')
    def validate_numero_factura(cls, v):
        if v is None:
            return 0  # Valor temporal que será reemplazado
        return v
    
    @field_validator('descuento')
    def validate_descuento(cls, v):
        if v < 0 or v > 100:
            raise ValueError("El descuento debe estar entre 0 y 100%")
        return v
    
    @field_validator('vlr_descuento')
    def validate_vlr_descuento(cls, v):
        if v < 0:
            raise ValueError("El valor del descuento no puede ser negativo")
        return v

    model_config = {
        'populate_by_name': True  # Actualizado desde allow_population_by_field_name
    }

    def to_dict(self):
        return {
            "factura": self.numero_factura,
            "fecha": self.fecha.isoformat(),  # Updated format
            "placa": self.placa,
            "categoria": self.categoria.capitalize(),
            "grupo": self.grupo,
            "cliente": self.id_cliente,
            "medio_pago": self.medio_pago,  # Asegurar que usamos la misma clave que en CSV
            "descuento": self.descuento,
            "vlr_descuento": self.vlr_descuento,
            "subtotal": self.subtotal,
            "total": self.total,
            "servicios": [
                {
                    "servicio": servicio.id_servicio,
                    "cantidad": servicio.cantidad,
                    "descripcion": servicio.descripcion,
                    "valor": servicio.valor
                } for servicio in self.servicios
            ]
        }