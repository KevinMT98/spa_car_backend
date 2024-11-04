from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ClienteServices import ClientesServices
from Core.Models.ClienteModel import ClienteModel
from utilidades import config

router = APIRouter()

@router.get("/", tags=["Clientes"])
async def clientes():
    ClientesServices.cargar_datos()
    content = [cliente.to_dict() for cliente in ClientesServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

@router.get('/buscar/{cedula}', tags=["Clientes"])
async def clientes_buscar(cedula: str):
    cliente = ClientesServices.buscar(cedula=cedula)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=config.Headers)

@router.post("/agregar/", tags=["Clientes"])
async def clientes_agregar(cliente: ClienteModel):
    resultado = ClientesServices.agregar(cliente)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.put("/actualizar/", tags=["Clientes"])
async def clientes_actualizar(cliente: ClienteModel):
    resultado = ClientesServices.actualizar(cliente)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("/eliminar/{cedula}", tags=["Clientes"])
async def clientes_eliminar(cedula: str):
    resultado = ClientesServices.eliminar(cedula)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)