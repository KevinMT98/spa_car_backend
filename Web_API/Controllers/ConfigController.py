from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from Core.Services.ConfigService import ConfigService
from utilidades import config

router = APIRouter()

@router.get("", tags=["Configuracion"])
async def obtener_config():
    """Obtener la configuración actual"""
    try:
        configuracion = ConfigService.obtener_config()
        return JSONResponse(content=configuracion.model_dump(), headers=config.Headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("", tags=["Configuracion"])
async def actualizar_config(actualizaciones: Dict[str, Any]):
    """Actualizar configuración parcialmente"""
    try:
        configuracion = ConfigService.actualizar_config(actualizaciones)
        return JSONResponse(content=configuracion.model_dump(), headers=config.Headers)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/reset", tags=["Configuracion"])
async def restablecer_config():
    """Restablecer configuración a valores por defecto"""
    try:
        configuracion = ConfigService._crear_config_default()  # Usar método correcto
        ConfigService.guardar_config(configuracion)  # Guardar la configuración default
        return JSONResponse(
            content={"mensaje": "Configuración restablecida", "config": configuracion.dict()},
            headers=config.Headers
        )
    except Exception as e:
        print(f"Error resetting config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al restablecer la configuración"
        )

