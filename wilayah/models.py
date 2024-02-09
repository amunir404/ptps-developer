from django.db import models


# Create your models here.
class Provinsi(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class KabKota(models.Model):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Kecamatan(models.Model):
    kabkota = models.ForeignKey(KabKota, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class KelDesa(models.Model):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.SET_NULL, null=True)
    kabkota = models.ForeignKey(KabKota, on_delete=models.SET_NULL, null=True)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tps(models.Model):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.SET_NULL, null=True)
    kabkota = models.ForeignKey(KabKota, on_delete=models.SET_NULL, null=True)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.SET_NULL, null=True)
    keldesa = models.ForeignKey(KelDesa, on_delete=models.SET_NULL, null=True)
    no = models.IntegerField()
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.no}"

    class Meta:
        unique_together = ("keldesa", "no")
