import sys
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.exceptions import HTTPException

from app.fibonacci import model, config

router = APIRouter(prefix="/fibonacci")


class ReturnType(Enum):
    NUMBER = "number"
    STRING = "string"
    AUTO = "auto"


@router.get("/{n}")
def fibonacci(n: Annotated[int, Path(title="The fibonacci number to get", ge=0, le=config.max_number)],
              return_type: ReturnType = ReturnType.AUTO) -> int | float | str:
    """ Returns the n-th fibonacci number. """
    number = model.get_fibonacci_number(n)
    if return_type == ReturnType.STRING:
        return str(number)
    if return_type == ReturnType.NUMBER and number > sys.float_info.max:
        message = f"The {n}th fibonacci number is too large to be returned as a number. Set return_type to string or auto."
        raise HTTPException(status_code=400, detail=message)
    if number > sys.float_info.max:
        return str(number)
    return number
