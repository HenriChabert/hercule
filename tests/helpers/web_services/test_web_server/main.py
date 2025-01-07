import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

current_dir = os.path.dirname(os.path.abspath(__file__))

def create_static_web_server() -> FastAPI:
    # Define a new FastAPI app specifically for testing
    test_app = FastAPI()
    test_app.mount("/", StaticFiles(directory=f"{current_dir}/static"), name="static")

    return test_app
