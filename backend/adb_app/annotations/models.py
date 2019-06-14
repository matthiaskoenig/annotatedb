from django.db import models


class Collection(models.Model):
    """ Collection.

    A data source for annotations.
    """
    namespace = models.CharField(max_length=40, unique=True)
    miriam = models.BooleanField()
    name = models.CharField(max_length=200, unique=True)
    idpattern = models.CharField(max_length=40)
    urlpattern = models.CharField(max_length=40)

    class Meta:
        pass
        # db_table = "collection"

    def __str__(self):
        return self.namespace


class Evidence(models.Model):
    """ Annotation evidence. """
    DATABASE = 'database'
    INFERENCE = 'inference'
    EVIDENCE_CHOICES = [
        (DATABASE, 'database'),
        (INFERENCE, 'inference'),
    ]

    source = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    evidence = models.CharField(max_length=40, choices=EVIDENCE_CHOICES)

    class Meta:
        # db_table = "evidence"
        unique_together = [['source', 'version']]


class Annotation(models.Model):
    """ Annotation.

    A single annotation.
    """
    term = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        # db_table = "annotation"
        unique_together = [['term', 'collection']]

        indexes = [
            models.Index(fields=['term', 'collection']),
            models.Index(fields=['term'], name='collection'),
        ]

    def __str__(self):
        return str(self.collection) + "/" + self.term

    @property
    def resource(self):
        return self.collection.urlpattern + self.term


class Mapping(models.Model):
    """ Annotation Mapping. """
    IS = 'IS'
    IS_VERSION_OF = 'IS_VERSION_OF'
    QUALIFIER_CHOICES = [
        (IS, 'IS'),
        (IS_VERSION_OF, 'IS_VERSION_OF'),
    ]
    source = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="mapping_source")
    qualifier = models.CharField(max_length=20, choices=QUALIFIER_CHOICES)
    target = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="mapping_target")
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)

    class Meta:
        pass
        #db_table = "mapping"