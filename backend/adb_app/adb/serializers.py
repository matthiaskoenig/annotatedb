from rest_framework import serializers
from .models import Collection, Evidence, Annotation, Mapping
import re


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

    def validate(self, data):
        """
        Check that annotion term matches the pattern.
        """
        collection = Collection.objects.get(namespace=data['collection'])
        pattern = collection.idpattern
        p = re.compile(pattern)

        m = p.match(data['term'])
        if not m:
            raise serializers.ValidationError(
                f"Annotation term `{data['term']}` does not follow pattern "
                f"`{pattern}`for collection `{collection}.`")

        return data


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