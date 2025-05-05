from django import forms
from .models import Pista

class PistaForm(forms.ModelForm):
    class Meta:
        model = Pista
        fields = ['nombre', 'tipo_pista']  
