from django import forms

from accounts.models import EndReport, StartReport, UserProfile, WhetherReport
from laporanhasil.models import Lhp, LhpMedia
from perolehansuara.models import PpwpMedia


class StartReportForm(forms.ModelForm):
    start_date = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "py-2.5 text-base fw-bold peer form-checkbox rounded-full",
                "checked": "checked",
                "type": "hidden",
            }
        ),
    )

    class Meta:
        model = StartReport
        fields = ["start_date"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_date = True
        if commit:
            instance.save()
        return instance


class EndReportForm(forms.ModelForm):
    end_date = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "py-2.5 text-base fw-bold peer form-checkbox rounded-full",
                "checked": "checked",
                "type": "hidden",
            }
        ),
    )

    class Meta:
        model = EndReport
        fields = ["end_date"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.end_date = True
        if commit:
            instance.save()
        return instance


class LHPForm(forms.ModelForm):
    MASA_TENANG = 1
    PERSIAPAN_PEMUNGUTAN_SUARA = 2
    PEMUNGUTAN_DAN_PENGHITUNGAN = 3
    PENGAWASAN_LAINNYA = 3

    TAHAPAN_CHOICES = [
        ("", "Pilih Tahapan Pemilihan Umum"),
        (MASA_TENANG, "Masa Tenang"),
        (PERSIAPAN_PEMUNGUTAN_SUARA, "Persiapan Pemungutan Suara"),
        (PEMUNGUTAN_DAN_PENGHITUNGAN, "Pemungutan dan Penghitungan Suara"),
        (PENGAWASAN_LAINNYA, "Pengawasan Lainnya"),
    ]

    LANGSUNG = 1
    TIDAK_LANGSUNG = 2

    BENTUK_CHOICES = [
        ("", "Pilih Bentuk Pengawasan"),
        (LANGSUNG, "Langsung"),
        (TIDAK_LANGSUNG, "Tidak Langsung"),
    ]

    tahapan = forms.ChoiceField(
        required=True,
        choices=TAHAPAN_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "py-2.5 text-base fw-bold form-select text-white-dark flex-1",
            }
        ),
    )
    bentuk = forms.ChoiceField(
        required=True,
        choices=BENTUK_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "py-2.5 text-base fw-bold form-select text-white-dark flex-1",
            }
        ),
    )

    tujuan = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1 ",
                "placeholder": "Masukan Tujuan Kegiatan Pengawasan",
                "type": "text",
            },
        ),
    )
    sasaran = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1",
                "placeholder": "Masukan Sasaran Kegiatan Pengawasan",
                "type": "text",
            },
        ),
    )
    waktu = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1",
                "type": "datetime-local",
            },
        ),
    )
    tempat = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1",
                "placeholder": "Masukan Nama Tempat Kegiatan Pengawasan",
                "type": "text",
            },
        ),
    )
    uraian = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 20,
                "class": "py-2.5 text-base fw-bold form-textarea flex-1",
                "placeholder": "Masukan Uraian singkat Pengawasan disini",
            }
        ),
    )

    class Meta:
        model = Lhp

        fields = ["tahapan", "bentuk", "tujuan", "sasaran", "waktu", "tempat", "uraian"]


class LHPMediaForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1",
                "type": "file",
            }
        ),
    )

    class Meta:
        model = LhpMedia
        fields = ["image"]


class WhetherReportForm(forms.ModelForm):
    CERAH = 1
    MENDUNG = 2
    HUJAN = 3

    WHETHER_CHOICES = [
        (CERAH, "Cerah"),
        (MENDUNG, "Mendung"),
        (HUJAN, "Hujan"),
    ]

    status = forms.ChoiceField(
        required=True,
        choices=WHETHER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "py-2.5 text-base fw-bold form-select text-white-dark flex-1",
            }
        ),
    )

    class Meta:
        model = WhetherReport
        fields = ["status"]


class PpwpMediaForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1",
                "type": "file",
            }
        ),
    )

    class Meta:
        model = PpwpMedia
        fields = ["image"]


class UserProfileForm(forms.ModelForm):
    LAKI_LAKI = 1
    PEREMPUAN = 2

    JK_CHOICES = [
        (LAKI_LAKI, "Laki-laki"),
        (PEREMPUAN, "Perempuan"),
    ]
    jk = forms.ChoiceField(
        required=False,
        choices=JK_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "py-2.5 text-base fw-bold form-select text-white-dark flex-1",
            }
        ),
        label="Jenis Kelamin",
    )

    alamat = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1 ",
                "placeholder": "Masukan Alamat Lengkap",
                "type": "text",
            },
        ),
    )
    rt = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1 ",
                "placeholder": "Masukan RT",
                "type": "text",
            },
        ),
    )
    rw = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1 ",
                "placeholder": "Masukan RW",
                "type": "text",
            },
        ),
    )
    wa = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "py-2.5 text-base fw-bold form-input flex-1 ",
                "placeholder": "Masukan No WhatsApp",
                "type": "text",
            },
        ),
        label="WhatsApp",
    )

    class Meta:
        model = UserProfile
        fields = ["jk", "alamat", "rt", "rw", "wa"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
