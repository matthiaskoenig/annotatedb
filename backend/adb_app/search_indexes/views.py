from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .documents import MappingDocument
from .serializers import MappingElasticSerializer


class MappingDocumentView(BaseDocumentViewSet):
    """The MappingDocument view."""

    document = MappingDocument
    serializer_class = MappingElasticSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'source.term',
        'source.collection.namespace',
        'source.collection.miriam',

        'qualifier',

        'target.namespace',
        'target.collection.namespace',
        'target.collection.miriam',

        'evidence.id',
        'evidence.source',
        'evidence.version',
        'evidence.evidence',
    )
    # Define filter fields
    filter_fields = {
        'id': 'id.raw'
    }
    ordering_fields = {
        'id': None,
    }
