# TerrainDetector
Automatic path planning for obstacles avoidance API for automatic leaf collector robot | KMITL Feedback control - Final project
-----
### Setting up in Raspberry PI
1. install all neccessary python libraries
     - `pip install websockets & asyncio`
     - `pip install opencv-python`
2. Copy or Download `client.py` from this repo

### Setting up in Local desktop or labtop
1. install cuda
2. install all libraries `pip install -r req.txt`
3. clone this repo using `git clone <this repo url>`

----
### How to use this API
#### Set ip address and port of both server and client
inside `client.py` at the lines
```python
async def main():
    async with connect("ws://localhost:1234") as ws:
```
change the `localhost` to your server's ip address (or the same network ip) also change `1234` to be the port same as server side.
<br><br>
inside `websocket_server.py`
```python
async def main():
    async with serve(handler, 'localhost', 1234):
        await asyncio.Future()
```
change `localhost` to ip address and change `1234` to your available port

#### How to send image to server side
In `client.py`
```python
img = cv2.resize(cv2.imread('./test.png'), (256, 256))
```
replace `cv2.imread('./test.png')` with numpy array like image. <br> Then just call the function with `asyncio.run(main())` every time you would like to use this API

#### Result from the API
The server will return `list` with of direction

Value | Meaning
-----|-----
negative | turn left
positive | turn right
777 | either left or right
-777 | impossible to pass

the more possitive or negative means the more angle to turn in order to avoid obstacle in that direction

---
### Example and Explanation
1. Obstacle is on the right hand side

![](https://github.com/Falight539/TerrainDetector/blob/master/im_source/split_right.png)

As you can see, I've split image into small patches then find the possible way to move each row from bottom to top.
In this case, object is on the middle of half <b>'right hand side of image'</b> so, the robot have to <b>'take a left turn'</b> to avoid it.

The result from the server will be: `[0, 0, 0, 0, -20, -20, -20, -20]`

2. Obstacle is on the left hand side

![](https://github.com/Falight539/TerrainDetector/blob/master/im_source/split_left.png)

Result: `[0, 0, 0, 20, 30, 20, 20, 20]`

3. Obstracle is on the middle left

![](https://github.com/Falight539/TerrainDetector/blob/master/im_source/split_lil_left.png)

Result: `[0, 0, 0, 0, 0, 777, 50, 777]`





