from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Core.Services.ServicioServices import ServiciosServices
from Core.Models.ServicioModel import ServicesModel
from utilidades import config
import uuid

router = APIRouter(prefix="/servicios", tags=["Servicios"])

@router.get("")
async def get_servicios(id_servicio: str = None):
    if (id_servicio):
        servicio = ServiciosServices.obtener_todos(id_servicio=id_servicio)
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return JSONResponse(content=servicio.to_dict(), headers=config.Headers)
    ServiciosServices.cargar_datos()
    content = [servicio.to_dict() for servicio in ServiciosServices.lista]
    return JSONResponse(content=content, headers=config.Headers)

@router.get('/categoria/{categoria}')
async def get_servicios_por_categoria(categoria: str):
    servicios = ServiciosServices.obtener_por_categoria(categoria)
    content = [servicio.to_dict() for servicio in servicios]
    return JSONResponse(content=content, headers=config.Headers)

@router.post("/")
async def create_servicio(servicio: ServicesModel):
    try:
        repo = ServiciosServices()
        servicio.id_servicio = str(uuid.uuid4())[:8]
        
        # Validar que haya al menos una categoría y grupo de valores
        if not servicio.valores:
            raise HTTPException(status_code=400, detail="Debe especificar al menos una categoría con valores")
        
        for categoria in servicio.valores:
            if not categoria.grupos:
                raise HTTPException(
                    status_code=400, 
                    detail=f"La categoría {categoria.categoria} debe tener al menos un grupo de valores"
                )
        
        if repo.agregar(servicio):
            return {
                "message": "Servicio creado exitosamente",
                "id": servicio.id_servicio,
                "servicio": servicio.dict()
            }
        else:
            raise HTTPException(status_code=500, detail="Error al crear el servicio")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_servicio}")
async def update_servicio(servicio: ServicesModel):
    resultado = ServiciosServices.actualizar(servicio)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)

@router.delete("/{id_servicio}")
async def delete_servicio(id_servicio: str):
    resultado = ServiciosServices.eliminar(id_servicio)
    if "Error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return JSONResponse(content={"mensaje": resultado}, headers=config.Headers)