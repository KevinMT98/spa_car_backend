from pydantic import BaseModel, Field
from datetime import date 

class ClienteModel(BaseModel):
    cedula: str = Field(..., min_length=3, max_length=10)
    nombre: str
    apellido: str
    fec_nacimiento: date
    telefono: str
    correo_electronico: str

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
    
    
