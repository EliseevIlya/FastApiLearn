from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import EmailAlreadyExistsException


def setup_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(EmailAlreadyExistsException, email_exists_handler)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


async def email_exists_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={"error": "Email already exists"}
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_str = str(exc.orig)

    if "users_email_key" in error_str:
        return JSONResponse(
            status_code=400,
            content={"error": "Email already exists"}
        )

    return JSONResponse(
        status_code=400,
        content={"error": "Database error"}
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"}
    )
