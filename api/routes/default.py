# import asyncio
# from datetime import datetime


from app import app
import dash
from dash import html
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse
from fastapi import WebSocket

# @app.server.get("/fastapi-sse-test", response_class=EventSourceResponse)
# async def fastapi_sse_test():
#     """SSE endpoint test"""
#     while True:
#         await asyncio.sleep(1)
#         yield {
#             "timestamp": datetime.now().isoformat(),
#         }

# @app.server.websocket("/fastapi-ws-test")
# async def fastapi_ws_test(websocket: WebSocket):
"""WebSocket endpoint test"""
await websocket.accept()
try:
    while True:
        await asyncio.sleep(1)
        await websocket.send_json(
            {
                "timestamp": datetime.now().isoformat(),
            }
        )
except Exception:
    pass