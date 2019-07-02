import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import MappingDocument

class MappingDocumentSerializer(DocumentSerializer):
    """Serializer for the Mapping document."""

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = MappingDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'source',
            'qualifier',
            'target',
            'evidence',
        )