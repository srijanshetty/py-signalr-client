#!/usr/bin/python
# -*- coding: utf-8 -*-

# signalr_aio/transports/_transport.py

# python compatiblity for >3.10
try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

# -----------------------------------
# Internal Imports
from ._exceptions import ConnectionClosed
from ._parameters import WebSocketParameters
from ._queue_events import InvokeEvent, CloseEvent

# -----------------------------------
# External Imports
try:
    from ujson import dumps, loads
except ModuleNotFoundError:
    from json import dumps, loads
from websockets import connect
import asyncio

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    pass


class Transport:
    def __init__(self, connection):
        self._connection = connection
        self._ws_params = None
        self._conn_handler = None
        self.invoke_queue = None
        self.ws = None
        self._set_loop_and_queue()

    # ===================================
    # Public Methods

    def start(self):
        self._ws_params = WebSocketParameters(self._connection)
        self._connect()

    def send(self, message):
        asyncio.Task(self.invoke_queue.put(InvokeEvent(message)))

    def close(self):
        asyncio.Task(self.invoke_queue.put(CloseEvent()))

    # -----------------------------------
    # Private Methods

    def _set_loop_and_queue(self):
        self.invoke_queue = asyncio.Queue()

    def _connect(self):
        self._conn_handler = asyncio.ensure_future(self._socket())

    async def _socket(self):
        async with connect(
            self._ws_params.socket_url, extra_headers=self._ws_params.headers
        ) as self.ws:
            self._connection.started = True
            await self._master_handler(self.ws)

    async def _master_handler(self, ws):
        consumer_task = asyncio.ensure_future(self._consumer_handler(ws))
        producer_task = asyncio.ensure_future(self._producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_EXCEPTION,
        )

        for task in pending:
            task.cancel()

    async def _consumer_handler(self, ws):
        while True:
            message = await ws.recv()
            if len(message) > 0:
                data = loads(message)
                await self._connection.received.fire(**data)

    async def _producer_handler(self, ws):
        while True:
            try:
                event = await self.invoke_queue.get()
                if event is not None:
                    if event.type == "INVOKE":
                        await ws.send(dumps(event.message))
                    elif event.type == "CLOSE":
                        await ws.close()
                        while ws.open is True:
                            await asyncio.sleep(0.1)
                        else:
                            self._connection.started = False
                            break
                else:
                    break
                self.invoke_queue.task_done()
            except Exception as e:
                raise e
