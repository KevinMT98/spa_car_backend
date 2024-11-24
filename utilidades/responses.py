
from fastapi.responses import JSONResponse
from utilidades import config

def error_response(status_code: int, message: str, error_type: str = "Error"):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "type": error_type,
            "message": message,
            "code": status_code
        },
        headers=config.Headers
    )

def success_response(data, message: str = None, status_code: int = 200):
    content = {
        "status": "success",
        "code": status_code,
        "data": data
    }
    if message:
        content["message"] = message
        
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=config.Headers
    )