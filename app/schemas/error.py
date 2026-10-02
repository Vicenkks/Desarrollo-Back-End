from pydantic import BaseModel
from typing import List, Optional

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorData(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []


class ErrorResponse(BaseModel):
    error: ErrorData