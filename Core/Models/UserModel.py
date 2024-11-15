from pydantic import BaseModel, Field, field_validator
import re

class UserModel(BaseModel):
    usuario: str = Field(..., min_length=3, max_length=50)
    nombre: str = Field(..., min_length=3, max_length=50)
    apellido: str = Field(..., min_length=3, max_length=50)
    clave: str = Field(..., min_length=6)
    rol: str = Field(..., min_length=3, max_length=50)
    
    # @field_validator("clave")
    # def clave_correcta(cls, clave):
    #     # Expresión regular para validar la contraseña
    #     pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z\d])[A-Za-z\d@$!%*?&]{8,}$'
    #     if not re.match(pattern, clave):
    #         raise ValueError("La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una letra minúscula, un número y un carácter especial.")
    #     return clave