from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from core.models import Languages      

class UserForm(UserCreationForm):
    password1 = forms.PasswordInput(attrs={
        'max': '6'
    })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                ('Passwords don\'t match.'), code='Invalid')
        return cd['password2']


class LngForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название...'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код'
            }),
            "icon": forms.FileInput(attrs={
                "class": "blog_cover_input"
            }),
            "active": forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            "default": forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


