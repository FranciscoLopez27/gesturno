from django import forms
from .models import Solicitud


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ('tipo', 'fecha_inicio', 'fecha_termino', 'motivo', 'respaldo')
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
