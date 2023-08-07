from enum import Enum


class ErrorMassages(Enum):
    FIELD_REQUIRED = "{key} is required."
    INVALID_VALUE = "Invalid value {} {}."
    INVALID_PARAMETERS = "Invalid parameters"