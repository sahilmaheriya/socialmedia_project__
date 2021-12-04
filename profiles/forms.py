from django import forms
from django.forms import widgets
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'bio' : forms.Textarea(attrs={'class':'form-control'}),
            'avatar' : forms.FileInput(attrs={'class':'form-control'}),
        }