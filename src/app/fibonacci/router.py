import sys
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app import config, blacklist
from app.fibonacci import model
from app.fibonacci.model import FibonacciList

router = APIRouter(prefix="/fibonacci")


class ReturnType(Enum):
    NUMBER = "number"
    STRING = "string"
    AUTO = "auto"


@router.get("/{n}")
def fibonacci(n: Annotated[int, Path(title="The fibonacci number to get", ge=0, le=config.max_number)],
              return_type: ReturnType = ReturnType.AUTO) -> int | float | str:
    """ Returns the n-th fibonacci number. """
    if n in blacklist.blacklisted_numbers:
        raise HTTPException(status_code=403, detail=f"Number {n} is blacklisted.")
    number = model.get_fibonacci_number(n)
    if return_type == ReturnType.STRING:
        return str(number)
    if return_type == ReturnType.NUMBER and number > sys.float_info.max:
        message = f"The {n}th fibonacci number is too large to be returned as a number. Set return_type to string or auto."
        raise HTTPException(status_code=400, detail=message)
    if number > config.max_float:
        return str(number)
    return number


@router.get("/")
def fibonacci_list(page: Annotated[int, Query(ge=1)] = 1,
                   limit: Annotated[int, Query(ge=1, le=config.max_numbers_per_page)] = 100) -> FibonacciList:
    """ Returns a list of fibonacci numbers. """
    if (page - 1) * limit >= 10_000 and limit > 100:
        raise HTTPException(status_code=422,
                            detail="For large fibonacci numbers the maximum page limit is 100.")

    try:
        return FibonacciList(page=page, limit=limit,
                             fibonacci_numbers=[model.Fibonacci(index=i, number=model.get_fibonacci_number(i))
                                                for i in range((page - 1) * limit, min(config.max_number + 1, page * limit))
                                                if i not in blacklist.blacklisted_numbers])
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.json())
