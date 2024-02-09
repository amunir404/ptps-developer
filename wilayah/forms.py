from django import forms

from wilayah.models import KabKota, Kecamatan, KelDesa, Provinsi


class WilayahProvinsiForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Masukan Nama Provinsi",
                "type": "text",
                "autofocus": "True",
            },
        ),
    )

    class Meta:
        model = Provinsi
        fields = ["name"]


class WilayahKabKotaForm(forms.ModelForm):
    provinsi = forms.ModelChoiceField(
        required=True,
        queryset=Provinsi.objects.all(),
        empty_label="Pilih Provinsi",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Masukan Nama Kabupaten/Kota",
                "type": "text",
            },
        ),
    )

    class Meta:
        model = KabKota
        fields = ["name", "provinsi"]


class WilayahKecamatanForm(forms.ModelForm):
    provinsi = forms.ModelChoiceField(
        required=True,
        queryset=Provinsi.objects.all(),
        empty_label="Pilih Provinsi",
        widget=forms.Select(
            attrs={
                "id": "id_provinsi",
                "class": "form-control",
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
                "class": "form-control",
            }
        ),
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Masukan Nama Kabupaten/Kota",
                "type": "text",
            },
        ),
    )

    class Meta:
        model = Kecamatan
        fields = ["provinsi", "kabkota", "name"]

    def __init__(self, *args, **kwargs):
        super(WilayahKecamatanForm, self).__init__(*args, **kwargs)

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


class WilayahKelDesaForm(forms.ModelForm):
    provinsi = forms.ModelChoiceField(
        required=True,
        queryset=Provinsi.objects.all(),
        empty_label="Pilih Provinsi",
        widget=forms.Select(
            attrs={
                "id": "id_provinsi",
                "class": "form-control",
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
                "class": "form-control",
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
                "class": "form-control",
            }
        ),
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Masukan Nama Kelurahan Desa",
                "type": "text",
            },
        ),
    )

    class Meta:
        model = KelDesa
        fields = ["provinsi", "kabkota", "kecamatan", "name"]

    def __init__(self, *args, **kwargs):
        super(WilayahKelDesaForm, self).__init__(*args, **kwargs)

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
            self.fields[
                "kecamatan"
            ].queryset = self.instance.kabkota.kecamatan_set.all()
