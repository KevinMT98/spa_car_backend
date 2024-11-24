from fastapi import APIRouter, Query
from typing import Union
from Core.Services.ServicioServices import ServiciosServices
from Core.Models.ServicioModel import ServicioGeneralModel, ServicioAdicionalModel
from utilidades import config
from utilidades.responses import error_response, success_response


router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("", tags=["Servicios"])
async def obtener_servicios(
    tipo_servicio: str,
    id_servicio: Union[int, None] = Query(default=None),
    nombre: Union[str, None] = Query(default=None)
):
    """Obtener servicios por diferentes criterios"""
    try:
        if id_servicio is not None:
            resultado = ServiciosServices.consultar_por_id(tipo_servicio, id_servicio)
            if not resultado:
                return error_response(404, "Servicio no encontrado")
        elif nombre is not None:
            resultado = ServiciosServices.consultar_por_nombre(tipo_servicio, nombre)
            if not resultado:
                return error_response(404, "Servicio no encontrado")
        else:
            resultado = ServiciosServices.consultar_todos(tipo_servicio)

        return success_response(
            data=resultado,
            message="Servicios obtenidos exitosamente",
            status_code=200
        )
    except Exception as e:
        return error_response(500, str(e), "Error al obtener servicios")


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



