from fastapi import FastAPI
from Web_API.Controllers.Cliente_controller import router as cliente_router
from Web_API.Controllers.Auth_Controller import router as auth_router

app = FastAPI()

app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(auth_router, prefix="/auth", tags=["Usuarios"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)