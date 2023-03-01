from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse

from src.trace_client import TraceClient, get_trace_context
from src.metrics import setup_middleware

from src.logger import create_logger
from src.settings import get_settings
from src.state import State


state = State()
settings = get_settings()
logger = create_logger(serialized=settings.serialized_logger)

# Service init
app = FastAPI(title="ds-service-template", version="0.1.1")

# Set /health/liveness to True
state.set_live_status(True)

# Setup middleware for metrics collection
setup_middleware(app=app)

# Trace client init
tc = TraceClient(
    service_name=app.title,
    agent_host_name=settings.jaeger_host,
    agent_port=settings.jaeger_port,
    enabled=settings.jaeger_enabled,
)

# Set /health/readiness to True
state.set_ready_status(True)


@app.get("/test")
def foo():
    return 1


@app.get("/health/liveness")
def liveness(response: Response):
    """Liveness probe endpoint."""
    _status = state.get_live_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"liveness": _status}


@app.get("/health/readiness")
def readiness(response: Response):
    """Readiness probe endpoint."""
    _status = state.get_ready_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"readiness": _status}


@app.get("/")
def redirect_docs():
    """Redirect on SwaggerUI."""
    logger.info("Request to docs.")
    return RedirectResponse(url="/docs")


@app.on_event("shutdown")
def on_shutdown():
    """State managment on shutdown."""
    state.set_ready_status(False)
    state.set_live_status(False)
    logger.info("Service shuted down !")
