from fastapi import APIRouter
from typing import Union
from Core.Services.ServicioServices import ServiciosServices
from Core.Models.ServicioModel import ServicioGeneralModel, ServicioAdicionalModel
from utilidades import config
from utilidades.responses import error_response, success_response


router = APIRouter(prefix="/servicios", tags=["Servicios"])

@router.post("", tags=["Servicios"])
async def crear_servicio(servicio: ServicioGeneralModel | ServicioAdicionalModel):
    """Crear un nuevo servicio"""
    try:
        if isinstance(servicio, ServicioGeneralModel):
            resultado = ServiciosServices.agregarGeneral(servicio)
        elif isinstance(servicio, ServicioAdicionalModel):
            resultado = ServiciosServices.agregarAdicional(servicio)
        else:
            return error_response(400, "Tipo de servicio no válido")

        return success_response(
            data=None,
            message=resultado,
            status_code=201
        )
    except Exception as e:
        return error_response(500, str(e), "Error al crear servicio")

