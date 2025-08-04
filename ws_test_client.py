import asyncio
import websockets
import os

from dotenv import load_dotenv

load_dotenv()

WS_HOST = os.getenv('WS_HOST')
WS_PORT = int(os.getenv('WS_PORT'))

async def test_ws():  
    uri = "ws://" + WS_HOST + ":" + f"{WS_PORT}"
    async with websockets.connect(uri) as websocket:
        print("Connected.")
        try:
            while True:
                msg = await websocket.recv()
                print("Message:", msg)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed.")

asyncio.run(test_ws())

