from django import forms
from app.tipo_usuario.models import TipoUsuario

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)
    tipo_usuario = forms.ModelChoiceField(queryset=TipoUsuario.objects.all())

class LoginForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)
