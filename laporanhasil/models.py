from django.db import models

from accounts.models import User
from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.
class Lhp(models.Model):
    MASA_TENANG = 1
    PERSIAPAN_PEMUNGUTAN_SUARA = 2
    PEMUNGUTAN_DAN_PENGHITUNGAN = 3
    PENGAWASAN_LAINNYA = 3

    TAHAPAN_CHOICES = [
        (MASA_TENANG, "Masa Tenang"),
        (PERSIAPAN_PEMUNGUTAN_SUARA, "Persiapan Pemungutan Suara"),
        (PEMUNGUTAN_DAN_PENGHITUNGAN, "Pemungutan dan Penghitungan Suara"),
        (PENGAWASAN_LAINNYA, "Pengawasan Lainnya"),
    ]

    LANGSUNG = 1
    TIDAK_LANGSUNG = 2

    BENTUK_CHOICES = [
        (LANGSUNG, "Langsung"),
        (TIDAK_LANGSUNG, "Tidak Langsung"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    tahapan = models.IntegerField(choices=TAHAPAN_CHOICES)
    bentuk = models.IntegerField(choices=BENTUK_CHOICES)
    tujuan = models.CharField(max_length=255)
    sasaran = models.CharField(max_length=255)
    waktu = models.CharField(max_length=255)
    tempat = models.CharField(max_length=255)
    uraian = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tujuan


class LhpMedia(models.Model):
    lhp = models.ForeignKey(Lhp, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to="lhp/")

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.images)

        # Convert image to RGB mode if it's RGBA
        if im.mode == "RGBA":
            im = im.convert("RGB")

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((945, 2048))

        # Save the modified image to the output
        im.save(output, format="JPEG", quality=300)
        output.seek(0)

        # Change the image field value to be the newly modified image value
        self.images = InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.jpg" % self.images.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(output),
            None,
        )

        super().save(*args, **kwargs)
