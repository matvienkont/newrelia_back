from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.views import View
from rest_framework.viewsets import ViewSetMixin, ViewSet, ModelViewSet


class ReceiveImgView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        print("HEY")
        return Response("HEllo", headers={ "Access-Control-Allow-Origin" : "*"})


    def put(self, request, format=None):
        print(request)
        print(request.FILES)
        #file_obj = request.FILES['file']
        print("PUT")
        # do some stuff with uploaded file
        return Response("OK", headers={ "Access-Control-Allow-Origin" : "*"})
