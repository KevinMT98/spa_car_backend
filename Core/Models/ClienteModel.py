from pydantic import BaseModel, Field, field_validator,EmailStr
from datetime import date, datetime
from typing import Literal
import re

class ClienteModel(BaseModel):
    
    tipo_doc: Literal["CC","NIT","CE","PP","TI"]     
    documento: str = Field(..., min_length=3, max_length=15)
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=50)
    fec_nacimiento: date
    telefono: str = Field(..., min_length=7, max_length=15)
    email: EmailStr

   
    @field_validator("email")
    def email_valido(cls, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            raise ValueError("Correo electrónico inválido.")
        if not (email.endswith(('.com', '.co', '.edu', '.org')) or email.endswith(('.COM', '.CO', '.EDU', '.ORG'))):
            raise ValueError("El correo electrónico debe terminar con (.com), (.co), (.edu) o (.org)")
        return email

    
    @field_validator("fec_nacimiento")
    def parse_fecha_nacimiento(cls, fec_nacimiento):
        if isinstance(fec_nacimiento, str):
            try:
                return datetime.strptime(fec_nacimiento, "%Y-%m-%D").date()
            except ValueError:
                raise ValueError("La fecha de nacimiento debe tener el formato YYYY-MM-DD.")
        return fec_nacimiento

    @field_validator("fec_nacimiento")
    def fecha_nacimiento_valida(cls, fec_nacimiento):
        if fec_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede ser mayor a la fecha actual.")
        return fec_nacimiento    
        
    def to_dict(self):
        return {
            "Tipo de documento": self.tipo_doc,
            "Documento": self.documento,
            "Nombre": self.nombre,
            "Apellido": self.apellido,
            "Fecha nacimiento": self.fec_nacimiento.isoformat(),
            "Telefono": self.telefono,
            "Email": self.email
        }
        
    def __str__(self):
        return (
            f"Cliente({self.documento}, "
            f"{self.nombre}, {self.apellido}, "
            f"{self.fec_nacimiento}, {self.telefono}, "
            f"{self.email})"
        )
    
class Cliente:
    def __init__(self,tipo_doc,documento,nombre,apellido,fec_nacimiento,telefono,email):
        self.tipo_doc = tipo_doc
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.fec_nacimiento = fec_nacimiento
        self.telefono = telefono
        self.email = email
        
    def to_dict(self):
        return {
            "Tipo de documento": self.tipo_doc,
            "Documento": self.documento,
            "Nombre": self.nombre,
            "Apellido": self.apellido,
            "Fecha nacimiento": self.fec_nacimiento,
            "Telefono": self.telefono,
            "Email": self.email
        }

    def __str__(self):
        return (
            f"Cliente({self.documento}, "
            f"{self.nombre}, {self.apellido}, "
            f"{self.fec_nacimiento}, {self.telefono}, "
            f"{self.email})"
        )
    
    
