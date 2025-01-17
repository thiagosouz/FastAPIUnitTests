from fastapi.responses import JSONResponse
from fastapi import Request
from shared.exceptions import NotFound

async def not_found_exception_handler(_: Request, exc: NotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exc.name} não encontrado(a)."}
    )  