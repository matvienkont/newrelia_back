import base64
import asyncio
from importlib import reload
import pickle
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import sys


async def send_image_response(socket_object):
    path_to_watch = "/home/mataringaro/Pictures/newrelia/"
    imagePath = path_to_watch + "cat.png"
    task = asyncio.Task(start(socket_object))

    with open(imagePath, "rb") as image:
        data = image.read()
        base64_encoded = base64.b64encode(data)
        base64_message = base64_encoded.decode('utf-8')

    #print(base64_message)

    await socket_object.send({"type": "websocket.send",
                        "text": base64_message})

async def start(socket_object):
    observer = Observer()
    event_handler = ResponseToEvent(socket_object)
    observer.schedule(event_handler, "/home/mataringaro/Pictures/newrelia/", recursive=True)
    observer.start()
    while True:
        with open("../cfg.pickle", "rb") as handle:
            shared = pickle.load(handle)
        #print(shared["interrupted"])
        await asyncio.sleep(4)
    observer.join()


class ResponseToEvent(LoggingEventHandler):
    def __init__(self, socket_object):
        super().__init__()
        self.socket_object = socket_object

    def on_created(self, event):
        print("New file")
        print(event.src_path)

        with open(event.src_path, "rb") as image:
            data = image.read()
            base64_encoded = base64.b64encode(data)
            base64_message = base64_encoded.decode('utf-8')

        task = asyncio.run(send_message(self.socket_object, base64_message))


async def send_message(socket_object, message):
    await socket_object.send({"type": "websocket.send",
                                   "text": message})