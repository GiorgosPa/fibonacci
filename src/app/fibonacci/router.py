from fastapi import APIRouter

router = APIRouter(prefix="/fibonacci")


@router.get("/")
def fibonacci():
    return {"message": "Hello, Fibonacci!"}
