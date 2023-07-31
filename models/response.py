from pydantic import validator,BaseModel,constr
from datetime import datetime

class Exchange_Rates_Model(BaseModel):
    timestamp : int
    date : str
    base : str
    rates : dict

class Convert_Currency_Model(BaseModel):
    query : dict
    info : dict
    date : str
    result: float

class Remove_Currency_Model(BaseException):
   pass 