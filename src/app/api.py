import contextlib
import sys

from fastapi import FastAPI

from app.fibonacci import router as fibonacci_router
from app.fibonacci import model as fibonacci_model


def create() -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        sys.set_int_max_str_digits(50_000)
        fibonacci_model.compute_fibonacci_number()
        yield

    app = FastAPI(title="Fibonacci API.",
                  lifespan=lifespan)

    app.include_router(fibonacci_router.router)

    return app
