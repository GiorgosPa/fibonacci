import contextlib
import sys

from fastapi import FastAPI

from app import fibonacci, blacklist


def create() -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        sys.set_int_max_str_digits(50_000)
        fibonacci.compute_fibonacci_number()
        yield
        blacklist.blacklisted_numbers.clear()
        fibonacci.fibonacci_sequence.clear()

    app = FastAPI(title="Fibonacci API.",
                  lifespan=lifespan)

    app.include_router(fibonacci.router)
    app.include_router(blacklist.router)

    return app
