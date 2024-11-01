from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ClienteServices import ClientesServices
from Core.Models.ClienteModel import ClienteModel,Cliente
from utilidades import config 
from pydantic import BaseModel

app = FastAPI()

@app.get("/clientes/")
async def clientes():
    ClientesServices.cargar_datos()
    content = [cliente.to_dict() for cliente in ClientesServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

@app.get('/clientes/buscar/{cedula}')
async def clientes_buscar(cedula: str):
    cliente = ClientesServices.buscar(cedula=cedula)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=config.Headers)

@app.post("/clientes/agregar/")
async def clientes_agregar(cliente: ClienteModel):
    ClientesServices.agregar(cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=config.Headers)

# @app.put("/clientes/")
# async def clientes_actualizar(cliente: BaseModel):
#     ClientesServices.actualizar(cliente)
#     return JSONResponse(content=cliente.to_dict(), headers=config.Headers)
