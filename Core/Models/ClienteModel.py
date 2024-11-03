from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
import re

class ClienteModel(BaseModel):
    cedula: str = Field(..., min_length=3, max_length=10)
    nombre: str
    apellido: str
    fec_nacimiento: date
    telefono: str
    correo_electronico: str
    
    @field_validator("correo_electronico")
    def correo_electronico_valido(cls, correo_electronico):
        # Expresión regular para validar el correo electrónico
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, correo_electronico):
            raise ValueError("Correo electrónico inválido.")
        if not (correo_electronico.endswith('.com') or correo_electronico.endswith('.co')):
            raise ValueError("El correo electrónico debe terminar con (.com) o (.co)")
        return correo_electronico
    
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
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fec_nacimiento": self.fec_nacimiento.isoformat(),
            "telefono": self.telefono,
            "correo_electronico": self.correo_electronico
        }
        
    def __str__(self):
        return (
            f"Cliente({self.cedula}, "
            f"{self.nombre}, {self.apellido}, "
            f"{self.fec_nacimiento}, {self.telefono}, "
            f"{self.correo_electronico})"
        )
    

class Cliente:
    def __init__(self, cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.fec_nacimiento = fec_nacimiento
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fec_nacimiento": self.fec_nacimiento,
            "telefono": self.telefono,
            "correo_electronico": self.correo_electronico
        }

    def __str__(self):
        return (
            f"Cliente({self.cedula}, "
            f"{self.nombre}, {self.apellido}, "
            f"{self.fec_nacimiento}, {self.telefono}, "
            f"{self.correo_electronico})"
        )
    
    
