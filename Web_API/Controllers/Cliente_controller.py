from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ClienteServices import ClientesServices
from Core.Models.ClienteModel import ClienteModel
from utilidades import config

router = APIRouter()

@router.get("", tags=["Clientes"])
async def clientes(documento: str = None):
    if documento:
        cliente = ClientesServices.buscar(documento=documento)
        if not cliente:         
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return JSONResponse(content=cliente, headers=config.Headers)
    ClientesServices.cargar_datos()
    content = [cliente.to_dict() for cliente in ClientesServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

# @router.get('/buscar/{documento}', tags=["Clientes"])
# async def clientes_buscar(documento: str):
#     cliente = ClientesServices.buscar(documento=documento)
#     if not cliente:
#         raise HTTPException(status_code=404, detail="Cliente no encontrado")
#     return JSONResponse(content=cliente.to_dict(), headers=config.Headers)

@router.post("", tags=["Clientes"])
async def clientes_agregar(cliente: ClienteModel):
    resultado = ClientesServices.agregar(cliente)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.put("", tags=["Clientes"])
async def clientes_actualizar(cliente: ClienteModel):
    resultado = ClientesServices.actualizar(cliente)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("", tags=["Clientes"])
async def clientes_eliminar(documento: str = None):
    
    resultado = ClientesServices.eliminar(documento)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)