from enum import enum


class BQB(Enum):
    IS = "BQB_IS"
    HAS_PART = "BQB_HAS_PART"
    IS_PART_OF = "BQB_IS_PART_OF"
    IS_VERSION_OF = "BQB_IS_VERSION_OF"
    HAS_VERSION = "BQB_HAS_VERSION"
    IS_HOMOLOG_TO = "BQB_IS_HOMOLOG_TO"
    IS_DESCRIBED_BY = "BQB_IS_DESCRIBED_BY"
    IS_ENCODED_BY = "BQB_IS_ENCODED_BY"
    ENCODES = "BQB_ENCODES"
    OCCURS_IN = "BQB_OCCURS_IN"
    HAS_PROPERTY = "BQB_HAS_PROPERTY"
    IS_PROPERTY_OF = "BQB_IS_PROPERTY_OF"
    HAS_TAXON = "BQB_HAS_TAXON"
    UNKNOWN = "BQB_UNKNOWN"


class Annotation(object):

    def __init__(self, relation, resource, description=None, label=None):
        self.relation = relation
        self.description = description
        self.label = label

        # get the collection/term part from identifiers.org urls
        for prefix in ["http://identifiers.org/", "https://identifiers.org/"]:
            if resource.startswith(prefix):
                resource = resource.replace(prefix, "")

        # other urls are directly stored as resources
        if resource.startswith("http"):
            self.collection = None
            self.term = resource
        else:
            # get term and collection
            tokens = resource.split("/")
            if len(tokens) < 2:
                raise ValueError(
                    f"resource `{resource}` must be of the form "
                    f"`collection/term` or an url starting with `http`)"
                )
            self.collection = tokens[0]
            self.term = "/".join(tokens[1:])

        self.validate()

    def to_dict(self):
        return {
            "term": self.term,
            "relation": self.relation.value,
            "collection": self.collection,
            "description": self.description,
            "label": self.label
        }

    @staticmethod
    def check_term(collection, term):
        """Checks that a given term follows id pattern for existing collection.

        :param collection:
        :param term:
        :return:
        """
        entry = MIRIAM_DICT.get(collection, None)
        if not entry:
            raise ValueError(
                f"MIRIAM collection `{collection}` does not exist for term `{term}`"
            )

        p = re.compile(entry['pattern'])
        m = p.match(term)
        if not m:
            raise ValueError(
                f"Term `{term}` did not match pattern "
                f"`{entry['pattern']}` for collection `{collection}`.")
            return False

        return True

    @staticmethod
    def check_qualifier(qualifier):
        """ Checks that the qualifier is an allowed qualifier.

        :param qualifier:
        :return:
        """
        if not isinstance(qualifier, BQB):
            raise ValueError(
                f"relation `{qualifier}``> is not in allowed qualifiers: "
                f"{[e.value for e in BQB]}")

    def validate(self):
        self.check_qualifier(self.relation)
        if self.collection:
            self.check_term(collection=self.collection, term=self.term)
