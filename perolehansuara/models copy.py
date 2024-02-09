from django.db import models
from accounts.models import User
from peserta_pemilu.models import DprdKabKota
from wilayah.models import Kecamatan, Tps


class SuaraPeserta(models.Model):
    tps = models.ForeignKey(Tps, on_delete=models.SET_NULL, null=True)
    nama_caleg = models.ForeignKey(DprdKabKota, on_delete=models.SET_NULL, null=True)
    suara = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tps




    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tps"], name="unique_tps_constraint")
        ]


class SuaraTps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tps = models.ForeignKey(Tps, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pemilih_dpt_lk = models.IntegerField(blank=True, null=True, default=0)
    pemilih_dpt_pm = models.IntegerField(blank=True, null=True, default=0)

    pengguna_dpt_lk = models.IntegerField(blank=True, null=True, default=0)
    pengguna_dpt_pm = models.IntegerField(blank=True, null=True, default=0)

    pengguna_dptb_lk = models.IntegerField(blank=True, null=True, default=0)
    pengguna_dptb_pm = models.IntegerField(blank=True, null=True, default=0)

    pengguna_dpk_lk = models.IntegerField(blank=True, null=True, default=0)
    pengguna_dpk_pm = models.IntegerField(blank=True, null=True, default=0)

    jml_terima = models.IntegerField(blank=True, null=True, default=0)
    jml_digunakan = models.IntegerField(blank=True, null=True, default=0)
    jml_dikembalikan = models.IntegerField(blank=True, null=True, default=0)
    jml_tidakdigunakan = models.IntegerField(blank=True, null=True, default=0)

    disabilitas_laki_laki = models.IntegerField(blank=True, null=True, default=0)
    disabilitas_wanita = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.tps.no}"
