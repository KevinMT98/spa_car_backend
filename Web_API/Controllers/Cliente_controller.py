from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ClienteServices import ClientesServices
from utilidades import config 

headers = config.Headers

app = FastAPI()

@app.get("/clientes/")
async def clientes():
    ClientesServices.cargar_datos()
    content = [cliente.to_dict() for cliente in ClientesServices.lista]
    return JSONResponse(content=content,headers=config.Headers)

@app.get('/clientes/buscar/{cedula}')
async def clientes_buscar(cedula: str):
    cliente = ClientesServices.buscar(cedula=cedula)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=config.Headers)

# Si decides implementar las funciones para agregar y actualizar, aquí están las bases:

# @app.post("/clientes/")
# async def clientes_agregar(cliente: BaseModel):
#     ClientesServices.agregar(cliente)
#     return JSONResponse(content=cliente.to_dict(), headers=headers)

# @app.put("/clientes/")
# async def clientes_actualizar(cliente: BaseModel):
#     ClientesServices.actualizar(cliente)
#     return JSONResponse(content=cliente.to_dict(), headers=headers)
