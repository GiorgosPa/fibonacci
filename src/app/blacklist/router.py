from typing import Annotated
from fastapi import APIRouter, Path, HTTPException

from app import config
from app.blacklist import model


router = APIRouter(prefix="/blacklist")


@router.post("/{number}")
def blacklist_number(number: Annotated[int, Path(title="The number to blacklist",
                                                 ge=0, le=config.max_number)]):
    """ Blacklists a number. """
    model.blacklist_number(number)


@router.delete("/{number}")
def whitelist_number(number: Annotated[int, Path(title="The number to whitelist",
                                                 ge=0, le=config.max_number)]):
    """ Whitelists a number. """
    try:
        model.whitelist_number(number)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Number {number} is not blacklisted.")
