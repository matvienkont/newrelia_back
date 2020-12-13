import base64
import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

#from demo.continuous_image_delivery import img_delivery
#from demo.ai_logic import interrupted
from .modules.send_image_response import send_image_response


class ImageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({"type": "websocket.accept"})


    async def websocket_receive(self, event):
        print("receive", event["text"])
        data = json.loads(event["text"])

        if(data["init"]):
            await send_image_response(self)

        #img_delivery()

        print("receive", event)


    async def websocket_disconnect(self, event):
        raise StopConsumer
        print("disconnected", event)