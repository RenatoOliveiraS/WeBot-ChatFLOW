from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AuthenticationError,
    BusinessError,
    DuplicateError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


async def business_exception_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def duplicate_exception_handler(request: Request, exc: DuplicateError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )
