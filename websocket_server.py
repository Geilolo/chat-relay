import asyncio
import os
import json
import redis
import websockets
from dotenv import load_dotenv

load_dotenv()

# Redis setup
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB"))
)

connected_clients = set()

async def message_sender(websocket):
    while True:
        # Pop the oldest message from Redis
        raw = r.lpop(f"chat:{os.getenv('TWITCH_CHANNEL')}")
        if raw:
            try:
                # Decode bytes → str
                raw_str = raw.decode("utf-8")

                # Clean up the string to be valid JSON
                json_str = raw_str.replace("'", '"')

                # Parse to dict
                message = json.loads(json_str)

                # Send to client
                await websocket.send(json.dumps(message))
            except Exception as e:
                print("Message format error:", e)
        else:
            await asyncio.sleep(1)  # wait a bit if nothing is in Redis

async def handler(websocket):
    connected_clients.add(websocket)
    print("Client connected.")
    try:
        await message_sender(websocket)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

