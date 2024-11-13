from pydantic import BaseModel, Field, field_validator
import re

class UserModel(BaseModel):
    usuario: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=50)
    lastname: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    rol: str = Field(..., min_length=3, max_length=50)
    
    # @field_validator("password")
    # def password_correcta(cls, password):
    #     # Expresión regular para validar la contraseña
    #     pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z\d])[A-Za-z\d@$!%*?&]{8,}$'
    #     if not re.match(pattern, password):
    #         raise ValueError("La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una letra minúscula, un número y un carácter especial.")
    #     return password