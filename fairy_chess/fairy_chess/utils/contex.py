from fastapi import Header
from starlette.requests import Request
from starlette_context import request_cycle_context


async def context_config(request: Request, token = Header(None)):
    data = {"token": token, "request": request}
    with request_cycle_context(data):
        yield