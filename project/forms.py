# forms.py 
from django import forms
from .models import *


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['name', 'image']


class BaseAdjustmentForm(forms.Form):
    is_gray_scale = forms.BooleanField(initial=False)


class RGBAdjustmentForm(forms.ModelForm):
    adjustment = forms.BooleanField(initial=False)
    r = forms.IntegerField(max_value=100, min_value=0)
    g = forms.IntegerField(max_value=100, min_value=0)
    b = forms.IntegerField(max_value=100, min_value=0)
