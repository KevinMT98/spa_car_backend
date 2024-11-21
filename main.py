from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Web_API.Controllers.Cliente_controller import router as cliente_router
from Web_API.Controllers.Auth_Controller import router as auth_router
from Web_API.Controllers.Vehiculo_controller import router as vehiculo_router
from Web_API.Controllers.Servicio_controller import router as servicio_router
from Web_API.Controllers.ConfigController import router as config_router


app = FastAPI(
    title="API de SPA CAR WASH",
    description="Esta API permite gestionar clientes, vehículos, realizar autenticación de usuarios y configuraciones de empresa",
    version="1.0.0"
)

app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(auth_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(vehiculo_router, prefix="/vehiculos", tags=["Vehículos"])
app.include_router(servicio_router, prefix="/servicios", tags=["Servicios"])
app.include_router(config_router, prefix="/configuracion", tags=["Configuracion"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen. Cambiar a dominios específicos en producción.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)