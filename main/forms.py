from django import forms
from .models import ImageModel
from django.forms import formset_factory
from django.contrib.auth.models import User

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

ImageFormSet = formset_factory(form=ImageForm, extra=3)