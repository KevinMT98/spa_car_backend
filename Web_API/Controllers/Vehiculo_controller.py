from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.VehiculoServices import VehiculoServices
from Core.Models.VehiculoModel import VehiculoModel
from utilidades import config

router = APIRouter()

@router.get("", tags=["Vehículos"])
async def obtener_vehiculos(placa: str = None, documento_cliente: str = None):
    if placa:
        vehiculo = VehiculoServices.buscar_placa(placa=placa)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")        
        return JSONResponse(content=vehiculo.to_dict(), headers=config.Headers)    
    if documento_cliente:
        vehiculos = VehiculoServices.buscar_cliente(documento_cliente=documento_cliente)
        if not vehiculos:
            raise HTTPException(status_code=404, detail="No se encontraron vehículos para el cliente")
        # Verifica si vehiculos es una lista o un solo objeto
        if isinstance(vehiculos, list):
            return JSONResponse(content=[vehiculo.to_dict() for vehiculo in vehiculos], headers=config.Headers)
        else:
            return JSONResponse(content=vehiculos.to_dict(), headers=config.Headers)
    
    VehiculoServices.cargar_datos()
    content = [vehiculo.to_dict() for vehiculo in VehiculoServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

# @router.get('/buscar/{placa}', tags=["Vehículos"])
# async def buscar_vehiculo(placa: str):
#     vehiculo = VehiculoServices.buscar(placa=placa)
#     if not vehiculo:
#         raise HTTPException(status_code=404, detail="Vehículo no encontrado")
#     return JSONResponse(content=vehiculo.to_dict(), headers=config.Headers)

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

@router.delete("", tags=["Vehículos"])
async def eliminar_vehiculo(placa: str = None):
    resultado = VehiculoServices.eliminar(placa)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)