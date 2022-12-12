import uptrace
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def tracing_config(app: FastAPI):
    uptrace.configure_opentelemetry(
        service_name="fairy_chess",
        service_version="0.1.0",
    )
    FastAPIInstrumentor.instrument_app(app)