from typing import Any, Literal, TypedDict

Status = Literal["OK", "INVALID_INPUT"]


class TimeRequest(TypedDict):
    wef: str
    unt: str


class Item(TypedDict):
    key: str
    value: str


class Parameters(TypedDict):
    item: Item


class InputValidationErrors(TypedDict):
    attributes: dict[str, Any]
    group: str
    category: str
    type: Literal["INVALID_ATTRIBUTE_VALUE"]
    parameters: Parameters


class InvalidInput(TypedDict):
    inputValidationErrors: InputValidationErrors
