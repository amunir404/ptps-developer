from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    CekPpwp,
    CekDpdRi,
    CekDprRi,
    CekDprdKabKota,
    CekDprdProv,
    PpwpMedia,
    DpdRiMedia,
    DprRiMedia,
    DprdKabKotaMedia,
    DprdProvMedia,
)


@receiver(post_save, sender=DprdProvMedia)
def post_dprdprov_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        CekDprdProv.objects.create(media=instance)
    else:
        try:

            cek_dprdprov = CekDprdProv.objects.get(media=instance)
            cek_dprdprov.save()
        except:
            CekDprdProv.objects.create(media=instance)


@receiver(post_save, sender=DprdKabKotaMedia)
def post_dprdkabkota_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        CekDprdKabKota.objects.create(media=instance)
    else:
        try:

            cek_dprdkabkota = CekDprdKabKota.objects.get(media=instance)
            cek_dprdkabkota.save()
        except:
            CekDprdKabKota.objects.create(media=instance)


@receiver(post_save, sender=DpdRiMedia)
def post_dpdri_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        CekDpdRi.objects.create(media=instance)
    else:
        try:

            cek_dpdri = CekDpdRi.objects.get(media=instance)
            cek_dpdri.save()
        except:
            CekDpdRi.objects.create(media=instance)


@receiver(post_save, sender=DprRiMedia)
def post_dprri_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        CekDprRi.objects.create(media=instance)
    else:
        try:

            cek_dprri = CekDprRi.objects.get(media=instance)
            cek_dprri.save()
        except:
            CekDprRi.objects.create(media=instance)


@receiver(post_save, sender=PpwpMedia)
def post_ptps_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        CekPpwp.objects.create(media=instance)
    else:
        try:

            cek_ppwp = CekPpwp.objects.get(media=instance)
            cek_ppwp.save()
        except:
            CekPpwp.objects.create(media=instance)
