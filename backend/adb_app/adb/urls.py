from rest_framework.routers import DefaultRouter

from .views import CollectionViewSet, EvidenceViewSet, AnnotationViewSet, MappingViewSet

router = DefaultRouter()
router.register("collections", CollectionViewSet, basename="collections")
router.register("evidences", EvidenceViewSet, basename="evidences")
router.register("annotations", AnnotationViewSet, basename="annotations")
router.register("mappings", MappingViewSet, basename="mappings")


