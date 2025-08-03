import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected.")
        try:
            while True:
                msg = await websocket.recv()
                print("Message:", msg)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed.")

asyncio.run(test_ws())

