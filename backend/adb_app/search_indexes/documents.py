from django.conf import settings
from django_elasticsearch_dsl import Document, fields, DEDField, Object, collections
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter

from adb_app.adb.models import Mapping


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

ngram_filter = token_filter(
    'ngram_filter',
    type="ngram",
    min_gram=1, max_gram=20
)

autocomplete = analyzer(
    'autocomplete',
    tokenizer="standard",
    filter=["lowercase", ngram_filter],
    char_filter=["html_strip"],
    chars=["letter"],
    token_chars=["letter"]
)

autocomplete_search = analyzer(
    'autocomplete_search',
    tokenizer="standard",
    filter=["lowercase"],
)


def string_field(attr, **kwargs):
    return fields.StringField(
        attr=attr,
        fielddata=True,
        analyzer=autocomplete,
        search_analyzer=autocomplete_search,
        fields={'raw': fields.KeywordField()},
        **kwargs
        )


class ObjectField(DEDField, Object):
    """ Custom ObjectField to work with nested object data.
        What is this needed for exactly.
    """

    def _get_inner_field_data(self, obj, field_value_to_ignore=None):
        data = {}
        if hasattr(self, 'properties'):
            for name, field in self.properties.to_dict().items():
                if not isinstance(field, DEDField):
                    continue

                if not field._path:
                    field._path = [name]

                data[name] = field.get_value_from_instance(
                    obj, field_value_to_ignore
                )
        else:
            for name, field in self._doc_class._doc_type.mapping.properties._params.get('properties', {}).items():  # noqa
                if not isinstance(field, DEDField):
                    continue

                if not field._path:
                    field._path = [name]

                data[name] = field.get_value_from_instance(
                    obj, field_value_to_ignore
                )

        return data

    def get_value_from_instance(self, instance, field_value_to_ignore=None):
        objs = super(ObjectField, self).get_value_from_instance(
            instance, field_value_to_ignore
        )

        if objs is None:
            return None
        if isinstance(objs, collections.Iterable):
            return [
                self._get_inner_field_data(obj, field_value_to_ignore)
                for obj in objs if obj != field_value_to_ignore
            ]

        return self._get_inner_field_data(objs, field_value_to_ignore)


# ------------------------------------
# Elastic Mapping Document
# ------------------------------------

@registry.register_document
class MappingDocument(Document):
    """ Elasticsearch document for mapping.

    This includes the information of the annotations, collections and evidence
    via ObjectFields.
    """

    id = fields.IntegerField(attr='id')

    source = fields.ObjectField(
        properties={
            'id': fields.IntegerField(attr="id"),
            'term': string_field(attr="term"),
            'collection': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(attr="id"),
                    'namespace': string_field(attr="namespace"),
                    'miriam': fields.BooleanField(attr="miriam"),
                }
            ),
        }
    )
    qualifier = string_field(attr="qualifier")
    target = fields.ObjectField(
        properties={
            'id': fields.IntegerField(attr="id"),
            'term': string_field(attr="term"),
            'collection': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(attr="id"),
                    'namespace': string_field(attr="namespace"),
                    'miriam': fields.BooleanField(attr="miriam"),
                }
            ),
        }
    )

    evidence = fields.ObjectField(
        properties={
            'id': fields.IntegerField("id"),
            'source': string_field("source"),
            'version': string_field("version"),
            'evidence': string_field("evidence")
        }

    )

    class Django(object):
        """Meta options."""
        model = Mapping  # The model associate with this DocType

        # Ignore auto updating of Elasticsearch when a model is saved or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }
