from django.db import models
from django.core.exceptions import ValidationError
import re


class Collection(models.Model):
    """ Collection.

    A data source for annotations.
    """
    namespace = models.CharField(max_length=40, unique=True)
    miriam = models.BooleanField()
    name = models.CharField(max_length=200, unique=True)
    idpattern = models.CharField(max_length=200)
    urlpattern = models.CharField(max_length=300)

    class Meta:
        pass

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
        unique_together = [['source', 'version']]


class Annotation(models.Model):
    """ Annotation.

    A single annotation.
    """
    term = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def clean(self, *args, **kwargs):
        # add custom validation here
        pattern = self.collection.idpattern
        p = re.compile(pattern)
        m = p.match(self.term)
        if not m:
            raise ValidationError(
                f"Annotation term `{self.term}` does not follow pattern "
                f"`{pattern}`for collection `{self.collection}.`")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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