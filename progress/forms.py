from progress.models import PassEntry
from django import forms


class PassEntryAddForm(forms.ModelForm):
    # location = forms.CharField(widget=YaMapWidget)

    class Meta:
        model = PassEntry
        fields = []


