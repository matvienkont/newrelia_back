import json
import asyncio
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.conf import settings
from django.views import View
from rest_framework.viewsets import ViewSetMixin, ViewSet, ModelViewSet
from multiprocessing import Pool
from channels.layers import get_channel_layer
#from modules.send_image_response import send_on_create
import threading
from GPUServer_connector import GPUserverAPI
from django.core.files.storage import default_storage
from channels.db import database_sync_to_async
import redis


class ReceiveImgView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        print("HEY")
        return Response("HEllo", headers={ "Access-Control-Allow-Origin" : "*"})

    def put(self, request, format=None):
        #print(request)
        imgs = request.FILES.getlist('file', None)
        print(imgs)
        #file_obj = request.FILES['file']
        print("PUT")
        # do some stuff with uploaded file
        print(request.data['data'])
        s = '{"style_imgs" : "style.jpg", "content_img": "content.jpg", "style_imgs_weights" : "1", "tv_weight" : "5", "temporal_weight":"25", "original_colors":"True", "pooling_type" : "max"}'
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                           port=settings.REDIS_PORT, db=0)

        redis_instance.set('key1', request.data['data'])

        with default_storage.open('content/' + 'content.jpg', 'wb+') as destination:
            for chunk in imgs[0].chunks():
                destination.write(chunk)

        with default_storage.open('style/' + 'style.jpg', 'wb+') as destination:
             for chunk in imgs[1].chunks():
                 destination.write(chunk)

        j = json.loads(s)
        GPUserverAPI.SendContentImage('/content/connection/content/content.jpg')
        GPUserverAPI.SendStyleImage('/content/connection/style/style.jpg')

        #socket_object = get_channel_layer()
        print(4)
        #PreserializeThread.start()

        return Response("OK", headers={ "Access-Control-Allow-Origin" : "*"})

def send_on_create():
    foo()

async def foo():
    print("sEND")
    await asyncio.sleep(4)

class PreserializeThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(PreserializeThread, self).__init__(*args, **kwargs)

    def run(self):
        send_on_create()