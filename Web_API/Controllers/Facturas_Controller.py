from fastapi import APIRouter, HTTPException, Path, Query
from typing import List
from Core.Models.FacturaModel import Factura
from Core.Services.FacturaServices import FacturaServices
from utilidades.responses import success_response, error_response

router = APIRouter()

@router.get("", tags=["Facturas"])
async def get_facturas(factura_id: int = Query(None, title="ID de la factura")):
    if factura_id:
        factura = FacturaServices.get_by_id(factura_id)
        if not factura:
            return error_response(404, "Factura no encontrada", "NotFoundError")
        return success_response(factura, "Factura consultada exitosamente")
    facturas = FacturaServices.get_all()
    return success_response(facturas, "Facturas consultadas exitosamente")


@router.post("", tags=["Facturas"])
async def create_factura(factura: Factura):
    try:
        result = FacturaServices.create(factura)
        if isinstance(result, str):  # Error message
            raise HTTPException(status_code=500, detail=result)
        return success_response(result, "Factura creada exitosamente", 201)
    except Exception as e:
        return error_response(500, str(e), "CreacionError")

@router.put("/{factura_id}", tags=["Facturas"])
async def update_factura(
    factura_id: int,
    factura: Factura
):
    try:
        factura.numero_factura = factura_id
        result = FacturaServices.update(factura_id, factura)
        
        if isinstance(result, str) and "Error" in result:
            raise HTTPException(status_code=500, detail=result)
        return success_response(result, "Factura actualizada exitosamente")
    except ValueError as ve:
        return error_response(404, str(ve), "NotFoundError")
    except Exception as e:
        return error_response(500, str(e), "ActualizacionError")

@router.delete("/{factura_id}",tags=["Facturas"])
async def delete_factura(factura_id: int = Path(..., title="ID de la factura")):
    try:
        result = FacturaServices.delete(factura_id)
        if isinstance(result, str):  # Error message
            raise HTTPException(status_code=500, detail=result)
        if not result:
            return error_response(404, "Factura no encontrada", "NotFoundError")
        return success_response({"deleted": True}, "Factura eliminada exitosamente")
    except ValueError as ve:
        return error_response(404, str(ve), "NotFoundError")
    except Exception as e:
        return error_response(500, str(e), "EliminacionError")
