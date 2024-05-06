from django import forms
from .models import Evento
from .models import Usuario
from .models import RegistroEvento

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario o correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'capacidad_maxima']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RegistroEventoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvento
        fields = [] 