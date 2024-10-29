from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Core.Services.ClienteServices import Clientes
from utilidades.config import Headers

app = FastAPI()

@app.get("/clientes/")
async def clientes():
    content = [cliente.to_dict() for cliente in Clientes.lista]
    return JSONResponse(content=content, headers=Headers)

@app.get('/clientes/buscar/{cedula}')
async def clientes_buscar(cedula: str):
    cliente = Clientes.buscar(cedula=cedula)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=Headers)

# @app.post("/clientes/")
# async def clientes_agregar(cliente: BaseModel):
#     Clientes.agregar(cliente)
#     return JSONResponse(content=cliente.to_dict(), headers=Headers)

# @app.put("/clientes/")
# async def clientes_actualizar(cliente: BaseModel):
#     Clientes.actualizar(cliente)
#     return JSONResponse(content=cliente.to_dict(), headers=Headers)