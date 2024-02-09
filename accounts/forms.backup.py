from django import forms
from accounts.models import User, UserPengawasTps, UserProfile, UserSaksiTps
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from wilayah.admin import KabKota

from wilayah.models import Kecamatan, KelDesa, Provinsi, Tps


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6",
                "placeholder": "Masukan alamat email valid",
                "type": "email",
                "id": "email",
                "autofocus": "True",
            },
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6",
                "placeholder": "Masukan Password",
                "required": "True",
                "type": "password",
                "id": "password",
            },
        ),
    )

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    # captcha = CaptchaField(label='Masukkan huruf yang kamu lihat', required=True, error_messages={'invalid': 'Captcha tidak sesuai'})

    class Meta:
        model = User
        fields = ["email", "password"]


class RegisterUserForm(forms.ModelForm):
    fullname = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input",
                "placeholder": "Masukan Nama Lengkap",
                "type": "text",
                "id": "fullname",
                "autofocus": "True",
            },
        ),
    )
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input",
                "placeholder": "Masukan alamat email valid",
                "type": "email",
                "id": "email",
            },
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input",
                "placeholder": "Masukan Password",
                "required": "True",
                "type": "password",
                "id": "password",
            },
        ),
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input",
                "placeholder": "Masukan Ulangi Password",
                "required": "True",
                "type": "password",
                "id": "confirm_password",
            },
        ),
    )

    class Meta:
        model = User
        fields = ["fullname", "email", "password"]

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class RegisterPengawasTPSForm(forms.ModelForm):
    provinsi = forms.ModelChoiceField(
        required=True,
        queryset=Provinsi.objects.all(),
        empty_label="Pilih Provinsi",
        widget=forms.Select(
            attrs={
                "id": "id_provinsi",
                "class": "py-2.5 text-base fw-bold form-select text-white-dark",
            }
        ),
    )
    kabkota = forms.ModelChoiceField(
        required=True,
        queryset=KabKota.objects.none(),
        empty_label="Pilih Kabupaten/Kota",
        widget=forms.Select(
            attrs={
                "id": "id_kabkota",
                "class": "py-2.5 text-base fw-bold form-select text-white-dark",
            }
        ),
    )
    kecamatan = forms.ModelChoiceField(
        required=True,
        queryset=Kecamatan.objects.none(),
        empty_label="Pilih Kecamatan",
        widget=forms.Select(
            attrs={
                "id": "id_kecamatan",
                "class": "py-2.5 text-base fw-bold form-select text-white-dark",
            }
        ),
    )
    keldesa = forms.ModelChoiceField(
        required=True,
        queryset=KelDesa.objects.none(),
        empty_label="Pilih Kelurahan/Desa",
        widget=forms.Select(
            attrs={
                "id": "id_keldesa",
                "class": "py-2.5 text-base fw-bold form-select text-white-dark  ",
            }
        ),
    )
    tps = forms.ModelChoiceField(
        required=True,
        queryset=Tps.objects.none(),
        empty_label="Pilih Nomor TPS",
        widget=forms.Select(
            attrs={
                "id": "id_tps",
                "class": "py-2.5 text-base fw-bold form-select text-white-dark  ",
            }
        ),
    )

    class Meta:
        model = UserPengawasTps
        fields = ["provinsi", "kabkota", "kecamatan", "keldesa", "tps"]

    def __init__(self, *args, **kwargs):
        super(RegisterPengawasTPSForm, self).__init__(*args, **kwargs)

        if "provinsi" in self.data:
            try:
                provinsi_id = int(self.data.get("provinsi"))
                self.fields["kabkota"].queryset = KabKota.objects.filter(
                    provinsi_id=provinsi_id
                )
            except (ValueError, TypeError):
                pass
        # If the form is bound to an instance (for editing an existing record)
        elif self.instance.pk:
            self.fields["kabkota"].queryset = self.instance.provinsi.kabkota_set.all()

        if "kabkota" in self.data:
            try:
                kabkota_id = int(self.data.get("kabkota"))
                self.fields["kecamatan"].queryset = Kecamatan.objects.filter(
                    kabkota_id=kabkota_id
                )
            except (ValueError, TypeError):
                pass
        # If the form is bound to an instance (for editing an existing record)
        elif self.instance.pk:
            self.fields["kecamatan"].queryset = (
                self.instance.kabkota.kecamatan_set.all()
            )

        if "kecamatan" in self.data:
            try:
                kecamatan_id = int(self.data.get("kecamatan"))
                self.fields["keldesa"].queryset = KelDesa.objects.filter(
                    kecamatan_id=kecamatan_id
                )
            except (ValueError, TypeError):
                pass
        # If the form is bound to an instance (for editing an existing record)
        elif self.instance.pk:
            self.fields["keldesa"].queryset = self.instance.kecamatan.keldesa_set.all()

        # Handling the 'tps' field queryset
        if "keldesa" in self.data:
            try:
                keldesa_id = int(self.data.get("keldesa"))
                self.fields["tps"].queryset = Tps.objects.filter(keldesa_id=keldesa_id)
            except (ValueError, TypeError):
                pass
        # If the form is bound to an instance (for editing an existing record)
        elif self.instance.pk:
            self.fields["tps"].queryset = self.instance.keldesa.tps_set.all()
