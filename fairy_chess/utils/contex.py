from fastapi import Header
from starlette.requests import Request
from starlette_context import request_cycle_context


async def context_config(request: Request, x_client_id = Header(None)):
    data = {"x_client_id": x_client_id, "request": request}
    with request_cycle_context(data):
        yield