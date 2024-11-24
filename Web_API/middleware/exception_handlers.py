from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from json.decoder import JSONDecodeError
from utilidades import config

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    simplified_errors = []
    
    for error in exc.errors():
        # Obtener el campo que causó el error
        field = error["loc"][-1] if error.get("loc") else "unknown"
        
        # Crear un error más simple y descriptivo
        simplified_errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "type": "ValidationError",
            "message": "Error de validación en los datos enviados",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": simplified_errors
        },
        headers=config.Headers
    )

async def json_decode_exception_handler(request: Request, exc: JSONDecodeError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "type": "JsonDecodeError",
            "message": "Error en el formato JSON",
            "code": status.HTTP_400_BAD_REQUEST,
            "detail": str(exc)
        },
        headers=config.Headers
    )