from pydantic import validator, BaseModel, constr
from datetime import datetime


class ExchangeRateResponse(BaseModel):
    timestamp: int
    date: str
    base: str
    rates: dict


class ConvertCurrency(BaseModel):
    query: dict
    info: dict
    date: str
    result: float


class RemoveCurrency(BaseException):
    pass
