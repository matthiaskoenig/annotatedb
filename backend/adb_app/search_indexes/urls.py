from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import MappingDocumentView

router = DefaultRouter()
books = router.register(r'mapping',
                        MappingDocumentView,
                        basename='mappingdocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]
