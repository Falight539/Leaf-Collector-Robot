import asyncio
from websockets.client import connect

import base64
import cv2

async def main():
    async with connect("ws://localhost:1234") as ws:
        img = cv2.resize(cv2.imread('./test.png'), (256, 256))
        _, im_array = cv2.imencode('.png', img)
        im_byte = im_array.tobytes()
        encode_img = base64.b64encode(im_byte)
        await ws.send(encode_img)

        message = await ws.recv()
        print(message)

if __name__ == "__main__":
    asyncio.run(main())