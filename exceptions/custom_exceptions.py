from sanic.exceptions import SanicException


class DataNotFoundError(SanicException):
    pass


class EmptyList(SanicException):
    pass


class DataNotFoundInCSVError(SanicException):
    pass


class NoQueryParam(SanicException):
    pass
