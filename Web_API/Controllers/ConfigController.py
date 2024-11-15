from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from Core.Services.ConfigService import ConfigService

router = APIRouter()

@router.get("", tags=["Configuracion"])
async def get_config():
    """Obtener la configuración actual"""
    try:
        return ConfigService.cargar_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/", tags=["Configuracion"])
async def update_config(updates: Dict[str, Any]):
    """Actualizar configuración parcialmente"""
    try:
        return ConfigService.modificar_config(updates)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/reset", tags=["Configuracion"])
async def reset_config():
    """Resetear la configuración a valores por defecto"""
    try:
        default_config = ConfigService.configuracion_estandar()
        ConfigService.agregar(default_config)
        return default_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))