import contextlib
import sys

from fastapi import FastAPI

from app import fibonacci


def create() -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        sys.set_int_max_str_digits(50_000)
        fibonacci.compute_fibonacci_number()
        yield

    app = FastAPI(title="Fibonacci API.",
                  lifespan=lifespan)

    app.include_router(fibonacci.router)

    return app
