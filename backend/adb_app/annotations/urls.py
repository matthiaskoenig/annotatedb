from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from .views import CollectionViewSet, EvidenceViewSet, AnnotationViewSet, MappingViewSet

router = DefaultRouter()
router.register("collections", CollectionViewSet, base_name="collections")
router.register("evidences", EvidenceViewSet, base_name="evidences")
router.register("annotations", AnnotationViewSet, base_name="annotations")
router.register("mappings", MappingViewSet, base_name="mappings")


schema_view = get_swagger_view(title="ADB API")
