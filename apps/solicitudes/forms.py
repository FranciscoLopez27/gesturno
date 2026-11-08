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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Texto de la primera opción de la lista de tipos (por defecto sale en inglés)
        self.fields['tipo'].empty_label = 'Selecciona un tipo'


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
