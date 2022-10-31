from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import RegexField
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class']="form-control"
        self.fields["username"].widget.attrs['placeholder']="Nombre de usuario"
        self.fields["password"].widget.attrs['class']="form-control"
        self.fields["password"].widget.attrs['placeholder']="Contraseña"

class FormularioUsuario(forms.ModelForm):
    password1=forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))
    password2=forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))
    
    class Meta:
        model=Usuario
        fields=('email', 'password1', 'username', 'nombres', 'apellidos','phone_number', 'provincia')
        widgets={
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Correo electronico'
                }
            ),
            
            'nombres':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Nombre'
                }
            ),
            'apellidos':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Apellido'
                }
            ),
            'username':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Nombre de usuario'
                }
            ),
            'phone_number':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'ej. 67891234',
                    "pattern":"[0-9]{8}"
                }
            ),
            
            
            'provincia':forms.Select(
                attrs={
                    'class':'form-select',
                    'placeholder': 'Provincia',
                    "list":"datalistOptions"
                }
            ),
           
        }
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ResetPassWordForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Ingrese un username",
        "class":"form-control",
        "autocomplete":"off"

    }))
    def clean(self) :
        cleaned=super().clean()
        if not Usuario.objects.filter(username=cleaned["username"]).exists():
            raise forms.ValidationError("El usuario no existe")
        return cleaned

    def get_user(self):
        username=self.cleaned_data.get("username")
        return Usuario.objects.get(username=username)

class ChangePassWordForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Ingrese una contraseña",
        "class":"form-control",
        "autocomplete":"off"

    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Repita la contraseña",
        "class":"form-control",
        "autocomplete":"off"

    }))

    def clean(self) :
        cleaned=super().clean()
        password=cleaned["password"]
        confirmPassword=cleaned["confirm_password"]
        if password != confirmPassword:
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('Las contraseñas deben ser iguales')
        return cleaned