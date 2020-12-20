from django.conf.urls import url, include
from rest_framework import routers
from .views import ReceiveImgView

router = routers.DefaultRouter()
router.register('', ReceiveImgView, basename="ReceiveImg")

urlpatterns = [
    url('', ReceiveImgView.as_view())
]