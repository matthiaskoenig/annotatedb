from rest_framework.routers import DefaultRouter

from .views import CollectionViewSet, EvidenceViewSet, AnnotationViewSet, MappingViewSet

router = DefaultRouter()
router.register("collections", CollectionViewSet, base_name="collections")
router.register("evidences", EvidenceViewSet, base_name="evidences")
router.register("annotations", AnnotationViewSet, base_name="annotations")
router.register("mappings", MappingViewSet, base_name="mappings")


