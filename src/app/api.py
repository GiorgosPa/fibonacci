from fastapi import FastAPI

from app.fibonacci import router as fibonacci_router


def create() -> FastAPI:
    app = FastAPI(title="Fibonacci API.")

    app.include_router(fibonacci_router.router)

    return app
