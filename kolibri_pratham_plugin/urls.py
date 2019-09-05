from django.conf.urls import include
from django.conf.urls import url

from rest_framework import routers

from .api import DataStoreViewset

router = routers.SimpleRouter()
router.register(r'datastore', DataStoreViewset, base_name='datastore')

urlpatterns = [
    url(r'^', include(router.urls)),
]
