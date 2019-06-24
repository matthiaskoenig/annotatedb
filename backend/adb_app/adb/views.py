from rest_framework import viewsets

from .permissions import IsAdminUserOrReadOnly
from .models import Collection, Evidence, Mapping, Annotation
from .serializers import CollectionSerializer, EvidenceSerializer, MappingSerializer, \
    AnnotationSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = "namespace"


class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = "pk"


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = "pk"


class MappingViewSet(viewsets.ModelViewSet):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = "pk"
