from rest_framework import serializers
from .models import Collection, Evidence, Annotation, Mapping


class CollectionSerializer(serializers.ModelSerializer):
    """ Returns the existing collections."""
    class Meta:
        model = Collection
        fields = [
            "namespace",
            "miriam",
            "name",
            "idpattern",
            "urlpattern"
        ]


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = [
            "source",
            "version",
            "evidence"
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    collection = serializers.SlugRelatedField(
        slug_field="namespace",
        queryset=Collection.objects.all())

    class Meta:
        model = Annotation
        fields = [
            "term",
            "collection"
        ]


class MappingSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="term",
        queryset=Annotation.objects.all())

    target = serializers.SlugRelatedField(
        slug_field="term",
        queryset=Annotation.objects.all())

    evidence = serializers.PrimaryKeyRelatedField(
        queryset=Evidence.objects.all()
    )

    class Meta:
        model = Mapping
        fields = [
            "source",
            "qualifier",
            "target",
            "evidence"
        ]