from dotenv import load_dotenv
import os
import asyncio
import socketio

import log_reader
from main import LOGLEVEL

load_dotenv()

if LOGLEVEL == "DEBUG":
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)
else:
    sio = socketio.AsyncClient()

MINER_UUID = os.getenv('MINER_UUID')
USERNAME = os.getenv('USERNAME')
SOCKET_URL = os.getenv('SOCKET_URL')



@sio.event
async def send_health_update(data):
    await sio.emit('health_update',
                   (os.getenv('MINER_UUID'),
                    data)
                   )


@sio.event
async def disconnect():
    print('disconnected from server')



@sio.event
async def connect():
    print('connection established')
    await sio.emit('connect')


async def connect_server():
    await sio.connect(SOCKET_URL)
    print(sio.sid)


async def run():
    await sio.wait()