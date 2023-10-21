import asyncio
from websockets.server import serve

import base64
import numpy as np
import cv2

from TerrainAnalysis import path_planer

plan = path_planer.analyzer()

async def handler(ws):
    message = await ws.recv()
    im_bytes = base64.b64decode(message)
    im_array = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_array, flags=cv2.IMREAD_COLOR)
    if img.shape != (256, 256, 3):
        img = cv2.resize(img, (256, 256))
    
    resps = plan.predicted(img)

    resps = np.array(resps, dtype=np.int16).tobytes()
    await ws.send(resps)

async def main():
    async with serve(handler, 'localhost', 1234):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())