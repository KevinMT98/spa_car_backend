from fastapi import FastAPI
from Web_API.Controllers.Cliente_controller import router as cliente_router
from Web_API.Controllers.Auth_Controller import router as auth_router
from Web_API.Controllers.Vehiculo_controller import router as vehiculo_router

app = FastAPI(
    title="API de Gestión de Clientes, Vehículos y Autenticación",
    description="Esta API permite gestionar clientes, vehículos y realizar autenticación de usuarios.",
    version="1.0.0"
)

app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(auth_router, prefix="/auth", tags=["Usuarios"])
app.include_router(vehiculo_router, prefix="/vehiculos", tags=["Vehículos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)