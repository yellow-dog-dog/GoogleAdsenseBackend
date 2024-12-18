from typing import Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int
    data: Optional[Any]
    message: str