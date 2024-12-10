from typing import Any

import sqlalchemy
from fastapi import status
from fastapi.responses import JSONResponse

from app.schemas.res import ResponseModel


def create_response(data=None, message: str = "Success", code: int = status.HTTP_200_OK):
    if data is None:
        data = {}
    return JSONResponse(
        status_code=code,
        content=ResponseModel(code=code, data=data, message=message).model_dump()
    )

def handle_exceptions(e: Exception):
    if isinstance(e, sqlalchemy.exc.IntegrityError):
        return create_response(code=status.HTTP_400_BAD_REQUEST, message='数据完整性错误')
    elif isinstance(e, sqlalchemy.exc.DataError):
        return create_response(code=status.HTTP_400_BAD_REQUEST, message='数据错误')
    elif isinstance(e, sqlalchemy.exc.DatabaseError):
        return create_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='数据库错误')
    else:
        return create_response(code=status.HTTP_400_BAD_REQUEST, message=f'未知错误: {e}')