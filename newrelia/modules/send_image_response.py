import base64
import asyncio
import json
from importlib import reload
import pickle
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from datetime import datetime, timedelta
from multiprocessing import Pool
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import sys
from channels.db import database_sync_to_async
from PIL import Image


async def send_image_response(socket_object):

    # path_to_watch = "/home/mataringaro/Pictures/newrelia/"
    # imagePath = path_to_watch + "cat.png"
    task = asyncio.Task(start(socket_object))

    await socket_object.channel_layer.send(socket_object.channel_name, {"type": "send_channel_name",
                                                                        "text": {
                                                                            "channel_name": socket_object.channel_name}
                                                                        })
    #
    # with open(imagePath, "rb") as image:
    #     data = image.read()
    #     base64_encoded = base64.b64encode(data)
    #     base64_message = base64_encoded.decode('utf-8')
    #
    # #print(base64_message)
    #

    #
    # #
    #
    # #GPUserverAPI.SendContentImage('/home/osboxes/Downloads/content3.png')
    #
    # socket_object.channel_layer.send(socket_object.channel_name, {"type": "send_response",
    #     "text": { "data": base64_message,
    #               "channel_name": socket_object.channel_name }
    # })
    #
    # pool = Pool(processes=1)
    # GPUserverAPI.RunProcessing(j)
    # result = pool.apply_async(GPUserverAPI.RunProcessing,j)
    # #asyncio.run(

async def start(socket_object):
    observer = Observer()
    event_handler = ResponseToEvent(socket_object)
    observer.schedule(event_handler, "/content/connection/", recursive=True)
    await asyncio.sleep(8)
    observer.start()
    while True:
    #     with open("../cfg.pickle", "rb") as handle:
    #         shared = pickle.load(handle)
    #     #print(shared["interrupted"])
        await asyncio.sleep(4)
    observer.join()


class ResponseToEvent(LoggingEventHandler):
    def __init__(self, socket_object):
        super().__init__()
        self.socket_object = socket_object
        self.last_modified = datetime.now()
        self.invalid_img = True

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=15):
            return
        else:
            self.last_modified = datetime.now()

        img = Image.open(event.src_path)
        self.invalid_img = True

        while self.invalid_img:
            try:
                img.verify()
                self.invalid_img = False
                print('Valid image')
                print(event.src_path)
                with open(event.src_path, "rb") as image:
                    data = image.read()
                    base64_encoded = base64.b64encode(data)
                    base64_message = base64_encoded.decode('utf-8')

                task = asyncio.run(send_message(self.socket_object, base64_message))

            except Exception:
                print('Invalid image')

            asyncio.run(asyncio.sleep(2))

    def on_created(self, event):
        print("New file")
        print(event.src_path)

        with open(event.src_path, "rb") as image:
            data = image.read()
            base64_encoded = base64.b64encode(data)
            base64_message = base64_encoded.decode('utf-8')

        task = asyncio.run(send_message(self.socket_object, base64_message))


async def send_message(socket_object, message):
    try:
        await socket_object.channel_layer.send(socket_object.channel_name, {"type": "send_img",
                                                                            "text": {
                                                                                "msg": message}
                                                                            })
    except ValueError:
        print (ValueError)
