from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.VehiculoServices import VehiculoServices
from Core.Models.VehiculoModel import VehiculoModel
from utilidades import config

router = APIRouter()

@router.get("/", tags=["Vehículos"])
async def obtener_vehiculos():
    VehiculoServices.cargar_datos()
    content = [vehiculo.dict() for vehiculo in VehiculoServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

@router.get('/buscar/{id_vehiculo}', tags=["Vehículos"])
async def buscar_vehiculo(id_vehiculo: str):
    vehiculo = VehiculoServices.buscar(id_vehiculo=id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return JSONResponse(content=vehiculo.dict(), headers=config.Headers)

@router.post("/agregar/", tags=["Vehículos"])
async def agregar_vehiculo(vehiculo: VehiculoModel):
    resultado = VehiculoServices.agregar(vehiculo)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.put("/actualizar/", tags=["Vehículos"])
async def actualizar_vehiculo(vehiculo: VehiculoModel):
    resultado = VehiculoServices.actualizar(vehiculo)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("/eliminar/{id_vehiculo}", tags=["Vehículos"])
async def eliminar_vehiculo(id_vehiculo: str):
    resultado = VehiculoServices.eliminar(id_vehiculo)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)