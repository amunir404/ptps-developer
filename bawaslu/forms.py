from django import forms

from perolehansuara.models import CekDpdRi


class AccDpdRiForm(forms.ModelForm):
    status = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "py-2.5 text-base fw-bold peer form-checkbox rounded-full",
                "checked": "checked",
                "type": "hidden",
            }
        ),
    )

    class Meta:
        model = CekDpdRi
        fields = ["status"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_date = True
        if commit:
            instance.save()
        return instance
