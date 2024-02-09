from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from wilayah.models import KabKota, Kecamatan, KelDesa, Provinsi, Tps


class UserManager(BaseUserManager):
    def create_user(self, fullname, email, password=None):
        if not email:
            raise ValueError("Pengguna harus memiliki alamat email")

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, password):
        user = self.create_user(
            email=self.normalize_email(email), password=password, fullname=fullname
        )
        user.role = 1
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    BAWASLU = 1
    PENGAWAS_TPS = 2

    ROLE_CHOICES = [
        (BAWASLU, "Bawaslu"),
        (PENGAWAS_TPS, "Pengawas TPS"),
    ]
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=PENGAWAS_TPS)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def get_level(self):
        if self.role == 1:
            user_level = "Bawaslu"
        elif self.role == 2:
            user_level = "Pengawas TPS"
        return user_level


class UserProfile(models.Model):
    LAKI_LAKI = 1
    PEREMPUAN = 2

    JK_CHOICES = [
        (LAKI_LAKI, "Laki-laki"),
        (PEREMPUAN, "Perempuan"),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photo", blank=True, null=True
    )
    jk = models.IntegerField(choices=JK_CHOICES, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    rt = models.CharField(blank=True, null=True)
    rw = models.CharField(blank=True, null=True)
    wa = models.CharField(max_length=16, blank=True, null=True)
    pin_code = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1},{self.address_line_2}'

    def __str__(self):
        return self.user.fullname


class UserPengawasTps(models.Model):
    maker = models.ForeignKey(
        User,
        related_name="maker",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": 1},
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, limit_choices_to={"role": 2}
    )
    userprofile = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    provinsi = models.ForeignKey(
        Provinsi, on_delete=models.SET_NULL, null=True, blank=True
    )
    kabkota = models.ForeignKey(
        KabKota, on_delete=models.SET_NULL, null=True, blank=True
    )
    kecamatan = models.ForeignKey(
        Kecamatan, on_delete=models.SET_NULL, null=True, blank=True
    )
    keldesa = models.ForeignKey(
        KelDesa, on_delete=models.SET_NULL, null=True, blank=True
    )
    tps = models.ForeignKey(Tps, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.fullname


class WhetherReport(models.Model):
    CERAH = 1
    MENDUNG = 2
    HUJAN = 3

    WHETHER_CHOICES = [
        (CERAH, "Cerah"),
        (MENDUNG, "Mendung"),
        (HUJAN, "Hujan"),
    ]

    ptps = models.OneToOneField(UserPengawasTps, on_delete=models.CASCADE)
    status = models.IntegerField(choices=WHETHER_CHOICES, default=CERAH)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ptps.user.fullname


class StartReport(models.Model):
    ptps = models.OneToOneField(UserPengawasTps, on_delete=models.CASCADE)
    start_date = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ptps.user.fullname


class EndReport(models.Model):
    ptps = models.OneToOneField(UserPengawasTps, on_delete=models.CASCADE)
    end_date = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ptps.user.fullname
