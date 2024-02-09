from django.db import models
from accounts.models import User, UserPengawasTps
from wilayah.models import Kecamatan, Tps
from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


class PpwpMedia(models.Model):
    ptps = models.ForeignKey(
        UserPengawasTps, related_name="ppwp", default=None, on_delete=models.CASCADE
    )
    images = models.FileField(upload_to="ppwp/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ptps.tps}"

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


class DprRiMedia(models.Model):
    ptps = models.ForeignKey(
        UserPengawasTps, related_name="dprri", default=None, on_delete=models.CASCADE
    )
    images = models.FileField(upload_to="dpr/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ptps.tps}"

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


class DpdRiMedia(models.Model):
    ptps = models.ForeignKey(
        UserPengawasTps, related_name="dpdri", default=None, on_delete=models.CASCADE
    )
    images = models.FileField(upload_to="dpd/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ptps.tps}"

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


class DprdProvMedia(models.Model):
    ptps = models.ForeignKey(
        UserPengawasTps, related_name="dprdprov", default=None, on_delete=models.CASCADE
    )
    images = models.FileField(upload_to="dprdprov/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ptps.tps}"

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.images)

        # Convert image to RGB mode if it's RGBA
        if im.mode == "RGBA":
            im = im.convert("RGB")

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((1080, 1920))

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


class DprdKabKotaMedia(models.Model):
    ptps = models.ForeignKey(
        UserPengawasTps,
        related_name="dprdkabkota",
        default=None,
        on_delete=models.CASCADE,
    )
    images = models.FileField(upload_to="dprdkab/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ptps.tps}"

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


class CekPpwp(models.Model):
    media = models.ForeignKey(PpwpMedia, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CekDprRi(models.Model):
    media = models.ForeignKey(DprRiMedia, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CekDpdRi(models.Model):
    media = models.ForeignKey(DpdRiMedia, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CekDprdProv(models.Model):
    media = models.ForeignKey(DprdProvMedia, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CekDprdKabKota(models.Model):
    media = models.ForeignKey(DprdKabKotaMedia, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
