from django.contrib import admin

from adb_app.adb.models import Annotation, Mapping, Evidence, Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ('namespace',)
    fields = ('pk', 'namespace', 'miriam', 'name', 'idpattern', 'urlpattern')
    list_display = ('pk', 'namespace', 'miriam', 'name', 'idpattern', 'urlpattern')


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    fields = ('pk', 'source', 'version', 'evidence')
    list_display = ('pk', 'source', 'version', 'evidence')
    list_filter = ('source', 'evidence')


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    fields = ('pk', 'term', 'collection')
    list_display = ('pk', 'term', 'collection', 'resource')
    search_fields = ('term', 'collection')
    list_filter = ('collection',)


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    fields = ('pk', 'source', 'qualifier', 'target', 'evidence')
    list_display = ('pk', 'source', 'qualifier', 'target', 'evidence')


