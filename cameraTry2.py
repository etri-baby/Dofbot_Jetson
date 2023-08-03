import cv2 as cv
import base64
import asyncio
import websockets

async def publish_frame():
    cap = cv.VideoCapture(0)
    while True:
        _, frame = cap.read()
        _, buffer = cv.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        async with websockets.connect('ws://129.254.174.120:9002') as websocket:
            print("websocket connet success")
            await websocket.send(jpg_as_text)
            try:
                print("sending??")
                await websocket.send("hi, window")
            except:
                print("message send failed")
        # await asyncio.sleep(0.1)

try:
    asyncio.get_event_loop().run_until_complete(publish_frame())
except KeyboardInterrupt:
    pass