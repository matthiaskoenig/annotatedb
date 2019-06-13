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

    def __str__(self):
        return self.namespace


class Evidence(models.Model):
    """ Annotation evidence. """
    source = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    evidence = models.CharField(max_length=40)


    # FIXME: unique together source and version
    # FIXME: choice fields for evidence


class Annotation(models.Model):
    """ Annotation.

    A single annotation.
    """
    term = models.CharField(max_length=100, unique=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.collection) + "/" + self.term


class Mapping(models.Model):
    """ Annotation Mapping.

    """
    source = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="mapping_source")
    qualifier = models.CharField(max_length=20)
    target = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="mapping_target")
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)

    # FIXME: qualifier choices