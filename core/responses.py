from enum import Enum
from typing import Any


class ResponseMessages(Enum):
    SUCCESS = 1
    ERROR = 2


def get_response(message: ResponseMessages,
                 details: str, data: dict | None = None):
    response: dict[str, Any] = {"message": message.name, "details": details}

    if data:
        response["data"] = data

    return response


def success(details: str, data: dict | None = None):
    return get_response(ResponseMessages.SUCCESS, details, data)


def error(details: str, data: dict | None = None):
    return get_response(ResponseMessages.ERROR, details, data)
