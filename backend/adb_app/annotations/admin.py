from django.contrib import admin

from adb_app.annotations.models import Annotation, Mapping, Evidence, Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    fields = ('pk', 'namespace', 'miriam', 'name', 'idpattern', 'urlpattern')
    list_display = ('pk', 'namespace', 'miriam', 'name', 'idpattern', 'urlpattern')


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    fields = ('pk', 'source', 'version', 'evidence')
    list_display = ('pk', 'source', 'version', 'evidence')


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    fields = ('pk', 'term', 'collection')
    list_display = ('pk', 'term', 'collection', 'resource')


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    pass


