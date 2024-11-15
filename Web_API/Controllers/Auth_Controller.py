from fastapi import FastAPI, HTTPException, APIRouter, Path, Query
from fastapi.responses import JSONResponse
from Core.Services.AutenticacionService import AuthService
from Core.Models.UserModel import UserModel
from utilidades import config
from typing import List

router = APIRouter()


@router.get("", tags=["Usuarios"])
async def usuarios(usuario: str = None):
    """Obtener lista de usuarios o un usuario específico"""
    if usuario:
        user = AuthService.obtener_usuario(usuario)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario {usuario} no encontrado")
        return JSONResponse(content=user.dict(), headers=config.Headers)
        
    AuthService.cargar_usuarios()
    content = [user.dict() for user in AuthService.users]
    return JSONResponse(content=content, headers=config.Headers)

@router.post("", tags=["Usuarios"])
async def registrar_usuario(user: UserModel):
    """Registrar un nuevo usuario"""
    resultado = AuthService.registrar_usuario(user)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.post("/login/", tags=["Usuarios"])
async def login(
    usuario: str = Query(..., description="Username del usuario"),
    clave: str = Query(..., description="Contraseña del usuario")
):
    """Autenticar usuario"""
    if AuthService.verificar_credenciales(usuario, clave):
        return JSONResponse(content={"mensaje": "Ingreso exitoso"}, headers=config.Headers)
    raise HTTPException(status_code=401, detail="Usuario o contraseña inválida")

@router.put("/{usuario}", tags=["Usuarios"])
async def actualizar_usuario(
    usuario: str = Path(..., description="Username del usuario a actualizar"),
    user: UserModel = None
):
    """Actualizar información de usuario"""
    if user.usuario != usuario:
        raise HTTPException(status_code=400, detail="Username en URL no coincide con el body")
    
    resultado = AuthService.actualizar_usuario(user)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("/{usuario}", tags=["Usuarios"])
async def eliminar_usuario(usuario: str = Path(..., description="Username del usuario a eliminar")):
    """Eliminar un usuario"""
    resultado = AuthService.eliminar_usuario(usuario)
    if "Error" in resultado:
        raise HTTPException(status_code=404, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

