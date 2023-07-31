from pydantic import BaseModel, validator, Field
from pydantic_core import PydanticCustomError
from typing import Optional
from sanic import json
class Convert_Currency_Model(BaseModel):
    from_ : list = Field(..., alias='from')
    to : list
    amount : Optional[list]

    @validator('from_')
    def validate_from(cls,from_ ):
        if len(from_[0]) != 3 :
            raise ValueError(f"{from_} is not a Valid Currency")
        
    @validator('to')
    def validate_to(cls,to ):
        if len(to[0]) != 3 :
            raise ValueError(f"{to} is not a Valid Currency")
    
class Exchange_Rates_Model(BaseModel):
    symbols : Optional[list]=['INR']
    base : Optional[list]=['USD']
    interval : Optional[list]=[1]

    @validator('base')
    def validator_base(cls,base):
        if len(base[0])!=3:
            raise ValueError(f'{base[0]} is not a Valid Base Currency')
    
    @validator('interval')
    def validator_interval(cls,interval):
        if(int(interval[0])<1 or int(interval[0]) > 60):
            raise ValueError('intervel should be between 1 to 60')


class Remove_Currency_Model(BaseModel):
    currency : list 