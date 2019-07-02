from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer, token_filter

from adb_app.adb.models import Mapping

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)
autocomplete_search = analyzer(
    'autocomplete_search',
    tokenizer="standard",
    filter=["lowercase"],
)

ngram_filter = token_filter(
    'ngram_filter',
    type="ngram",
    min_gram=1, max_gram=20
)

autocomplete = analyzer('autocomplete',
    tokenizer="standard",
    filter=["lowercase", ngram_filter],
    char_filter=["html_strip"],
    chars=["letter"],
    token_chars=["letter"])


def string_field(attr, **kwargs):
    return fields.StringField(
        attr=attr,
        fielddata=True,
        analyzer=autocomplete,
        search_analyzer=autocomplete_search,
        fields={'raw': fields.KeywordField()},
        **kwargs
        )


def text_field(attr):
    return fields.TextField(
        attr=attr,
        fielddata=True,
        analyzer=autocomplete,
        search_analyzer=autocomplete_search,
        fields={'raw': fields.KeywordField()}
        )


@INDEX.doc_type
class MappingDocument(DocType):
    """Mapping Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    source = fields.ObjectField(
        properties={
            'pk': fields.IntegerField(),
            'collection': string_field("collection"),
            'term': string_field("term"),
        }
    )
    qualifier = string_field(attr="qualifier")
    target = fields.ObjectField(
        properties={
            'pk': fields.IntegerField(),
            'collection': string_field("collection"),
            'term': string_field("term"),
        }
    )
    evidence = fields.ObjectField(
        properties={
            'pk': fields.IntegerField(),
            'source': string_field("source"),
            'version': string_field("version"),
            'evidence': string_field("evidence")
        }

    )

    class Meta(object):
        """Meta options."""

        model = Mapping  # The model associate with this DocType