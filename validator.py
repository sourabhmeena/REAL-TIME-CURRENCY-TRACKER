from exceptions.custom_exceptions import *


class Validator:
    def __init__(self):
        pass


    async def validate_params(cls, *args, **kwargs ):   ''' [a,b,c] ,  {{a='abc',b='abc'},{c='abc',d='abc'}} '''
        for value in kwargs.values():
            if value is None:
                raise DataNotFoundError(message="Please Enter All Required Fields):", status_code=400)

