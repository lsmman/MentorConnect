from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"code": exc.status_code, "message": exc.detail, "detail": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=detail)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
        "code": 400,
        "message": "Bad request",
        "detail": exc.errors()
    })

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return await http_exception_handler(request, exc)
        except Exception as exc:
            return JSONResponse(status_code=500, content={
                "code": 500,
                "message": "Internal server error",
                "detail": str(exc)
            })
