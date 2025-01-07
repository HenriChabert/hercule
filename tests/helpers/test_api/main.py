import threading
from time import sleep

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .router import router


def run_test_server(app: FastAPI, host: str, port: int):
    """Runs a FastAPI app on a separate thread."""
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)

    # Run the server in a thread
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for the server to start
    while not server.started:
        sleep(0.1)
    
    return thread

def stop_test_server(thread: threading.Thread):
    thread.join(timeout=.1)

def find_free_port() -> int:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))  # Bind to a free port
    port = s.getsockname()[1]
    s.close()
    return port

def create_test_client() -> FastAPI:
    # Define a new FastAPI app specifically for testing
    test_app = FastAPI()
    test_app.mount("/", StaticFiles(directory="tests/helpers/test_api/static"), name="static")
    test_app.include_router(router)

    return test_app
