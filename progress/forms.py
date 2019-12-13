from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from progress.models import PassEntry
from django import forms


class PassEntryAddForm(forms.ModelForm):
    # location = forms.CharField(widget=YaMapWidget)

    class Meta:
        model = PassEntry
        fields = []


class CaptchaLoginForm(AuthenticationForm):
    captcha = ReCaptchaField()

    class Meta:
        fields = ('login', 'password', 'captcha')
