import asyncio
import websockets.server as serv


async def handler(ws):
    msg = await ws.recv()

    print("server received: " + str(msg))

    await ws.send("Response from server")


async def main():
    async with serv(handler, 'localhost', 1234):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())