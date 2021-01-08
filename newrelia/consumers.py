import base64
import json
import os
import asyncio
import threading

from channels.consumer import AsyncConsumer
from multiprocessing import Process
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
from channels.auth import get_user
from GPUServer_connector import GPUserverAPI
#from demo.continuous_image_delivery import img_delivery
#from demo.ai_logic import interrupted
from .modules.send_image_response import send_image_response, start
import redis
from django.conf import settings


class ImageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({"type": "websocket.accept"})
        print(self.scope['user'])

    async def websocket_receive(self, event):
        print("receive", event["text"])
        data = json.loads(event["text"])

        if(data["init"]):
            print(get_user(self.scope))
            # self.user = self.scope["user"]
            # self.user_room_name = "socket_for_user_" + str(self.user.id)  ##Notification room name
            # await self.channel_layer.group_add(
            #     self.user_room_name,
            #     self.channel_name
            # )
            print("true")
            await send_image_response(self)
        else:
            redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                               port=settings.REDIS_PORT, db=0)
            s = redis_instance.get('key1')

            j = json.loads(s)
            print(j)
            t = threading.Thread(target=GPUserverAPI.RunProcessing, args=[j])
            t.setDaemon(True)
            t.start()



    async def send_response(self, event):
        await self.send({"type": "websocket.send",
                             "text": json.dumps({ "data": event["text"]["data"],
                             "channel_name": event["text"]["channel_name"] }),
                         })

    async def send_channel_name(self, event):
        await self.send({"type": "websocket.send",
                             "text": json.dumps({
                             "channel_name": event["text"]["channel_name"] }),
                         })

    async def send_img(self, event):
        await self.send({"type": "websocket.send",
                             "text": json.dumps({
                                "img": True,
                                "img_src": event["text"]["msg"]
                             }),
                         })


    async def websocket_disconnect(self, event):
        raise StopConsumer
        print("disconnected", event)