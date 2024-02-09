from import_export import resources
from .models import KabKota, Provinsi


class KabKotaResource(resources.ModelResource):
    class Meta:
        model = KabKota
        fields = ("name", "provinsi")
        export_order = ("name", "provinsi")


class ProvinsiResource(resources.ModelResource):
    class Meta:
        model = Provinsi
        fields = ("id", "name")
        export_order = ("name", "provinsi")
