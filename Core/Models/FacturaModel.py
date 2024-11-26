from typing import List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional, Literal

class ServicioFactura(BaseModel):
    id_servicio: str = Field(alias='servicio', default="9999")
    cantidad: Optional[int] = 1
    descripcion: str
    valor: float

    @field_validator('id_servicio')
    def validate_id_servicio(cls, v):
        if not v:
            return "9999"
        return v

class Factura(BaseModel):
    numero_factura: Optional[int] = Field(None, alias='factura')  # Hacerlo opcional para actualizaciones
    fecha: datetime
    placa: str
    id_cliente: str = Field(alias='cliente')
    medio_pago: str = Field(alias='medio_pago')  # Cambiar alias para que coincida con CSV
    descuento: float = Field(default=0.0)
    servicios: List[ServicioFactura]

    @field_validator('numero_factura')
    def validate_numero_factura(cls, v):
        if v is None:
            return 0  # Valor temporal que será reemplazado
        return v

    model_config = {
        'populate_by_name': True  # Actualizado desde allow_population_by_field_name
    }

    def to_dict(self):
        return {
            "factura": self.numero_factura,
            "fecha": self.fecha.strftime("%Y%m%d"),  # Formato fecha como string YYYYMMDD
            "placa": self.placa,
            "cliente": self.id_cliente,
            "medio_pago": self.medio_pago,  # Asegurar que usamos la misma clave que en CSV
            "descuento": self.descuento,
            "servicios": [
                {
                    "servicio": servicio.id_servicio,
                    "cantidad": servicio.cantidad,
                    "descripcion": servicio.descripcion,
                    "valor": servicio.valor
                } for servicio in self.servicios
            ]
        }