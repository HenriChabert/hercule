from fastapi import FastAPI

from .router import router


def create_test_api() -> FastAPI:
    # Define a new FastAPI app specifically for testing
    test_app = FastAPI()
    test_app.include_router(router)

    return test_app
