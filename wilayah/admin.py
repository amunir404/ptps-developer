from django.contrib import admin
from wilayah.models import KelDesa, Kecamatan, KabKota, Provinsi, Tps
from import_export.admin import ImportExportModelAdmin


class TpsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "no",
        "keldesa",
        "kecamatan",
        "kabkota",
    )
    ordering = ("id",)

    def kecamatan(self, obj):
        return obj.keldesa.kecamatan.name

    def kabkota(self, obj):
        return obj.keldesa.kecamatan.kabkota.name


class KelDesaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "kecamatan",
        "kabkota",
    )
    ordering = ("id",)

    def kabkota(self, obj):
        return obj.kecamatan.kabkota.name


class KecamatanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "kabkota",
    )
    ordering = ("id",)


class KabKotaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "provinsi",
    )
    ordering = ("id",)


class ProvinsiAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    ordering = ("id",)


# Register your models here.
admin.site.register(Provinsi, ProvinsiAdmin)
admin.site.register(KabKota, KabKotaAdmin)
admin.site.register(Kecamatan, KecamatanAdmin)
admin.site.register(KelDesa, KelDesaAdmin)
admin.site.register(Tps, TpsAdmin)
