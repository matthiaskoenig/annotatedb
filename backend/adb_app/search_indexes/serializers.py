import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import MappingDocument
from ..adb.models import Mapping, Evidence, Annotation, Collection


# -----------------------------------------------------------
# ElasticSerializers
# -----------------------------------------------------------
class EvidenceElasticSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evidence
        fields = ("id", "source", "version", "evidence")


class CollectionElasticSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ("id", "namespace", "miriam")


class AnnotationElasticSerializer(serializers.ModelSerializer):
    collection = CollectionElasticSerializer()

    class Meta:
        model = Annotation
        fields = ("id", "term", "collection")


class MappingElasticSerializer(serializers.ModelSerializer):
    """Serializer for the Mapping document."""
    source = AnnotationElasticSerializer()
    target = AnnotationElasticSerializer()
    evidence = EvidenceElasticSerializer()

    class Meta(object):
        """Meta options."""
        model = Mapping

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'source',
            'qualifier',
            'target',
            'evidence'
        )
