from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ServicioServices import ServiciosServices
from Core.Models.ServicioModel import ServicioModel
from utilidades import config

router = APIRouter()

@router.get("/", tags=["Servicios"])
async def servicios():
    ServiciosServices.cargar_datos()
    content = [servicio.to_dict() for servicio in ServiciosServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

@router.get('/buscar/{id_servicio}', tags=["Servicios"])
async def servicios_buscar(id_servicio: str):
    servicio = ServiciosServices.buscar(id_servicio=id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return JSONResponse(content=servicio.to_dict(), headers=config.Headers)

@router.get('/tipo/{segmento}', tags=["Servicios"])
async def servicios_por_tipo(segmento: str):
    servicios = ServiciosServices.buscar_por_segmento(segmento)
    content = [servicio.to_dict() for servicio in servicios]
    return JSONResponse(content=content, headers=config.Headers)

@router.post("/agregar/", tags=["Servicios"])
async def servicios_agregar(servicio: ServicioModel):
    resultado = ServiciosServices.agregar(servicio)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.put("/actualizar/", tags=["Servicios"])
async def servicios_actualizar(servicio: ServicioModel):
    resultado = ServiciosServices.actualizar(servicio)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("/eliminar/{id_servicio}", tags=["Servicios"])
async def servicios_eliminar(id_servicio: str):
    resultado = ServiciosServices.eliminar(id_servicio)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)