from fastapi import FastAPI, HTTPException,APIRouter
from fastapi.responses import JSONResponse
from Core.Services.AutenticacionService import AuthService
from Core.Models.UserModel import UserModel
from utilidades import config

router = APIRouter()

@router.post("/usuario/registrar/", tags=["Usuarios"])
async def registrar_usuario(user: UserModel):
    resultado = AuthService.registrar_usuario(user)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.post("/usuario/login/", tags=["Usuarios"])
async def login(username: str, password: str):
    if AuthService.verificar_credenciales(username, password):
        return JSONResponse(content={"mensaje": "Ingreso exitoso"}, headers=config.Headers)
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña invalida")