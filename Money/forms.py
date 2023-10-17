from django import forms
from django.contrib.auth.models import User
from .models import TokenVerificacionCorreo, PerfilUsuario, Publicacion, Comentario, MensajePrivado, Pago
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django import forms
from .models import Publicacion, Contenido
from .models import Curso, Leccion


class TokenVerificacionCorreoForm(forms.ModelForm):
    class Meta:
        model = TokenVerificacionCorreo
        exclude = ['token']
        fields = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo_pago', 'usuario']


class MensajePrivadoForm(forms.ModelForm):
    class Meta:
        model = MensajePrivado
        fields = ['grupo', 'tipo', 'texto', 'emisor', 'receptor']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'usuario', 'publicacion', 'comentario_padre']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Campo de contraseña

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomRadioSelect(forms.RadioSelect):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Eliminar la opción vacía
        context['widget']['optgroups'] = [group for group in context['widget']['optgroups'] if group[0] or group[1]]
        return context
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nivel_educativo', 'ubicacion', 'fecha_nacimiento', 'genero', 'codigo_pais', 'numero_telefono']
        widgets = {
            'genero': forms.RadioSelect(choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Otro', 'Otro')]),
            'fecha_nacimiento': widgets.DateInput(attrs={'type': 'date'}),
            'nivel_educativo': forms.RadioSelect(choices=[('principiante', 'Principiante'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')]),
        }
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de Usuario',
            'autofocus': 'true',
        })
    )
    
    email = forms.EmailField(
        max_length=254, 
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electrónico',
        })
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        }),
        help_text="La contraseña debe contener al menos 8 caracteres."
    )
    
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# forms.py


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'precio', 'imagen']

class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'orden']
    
    # Agrega campos para el contenido
    tipo_contenido = forms.ChoiceField(
        choices=Contenido.TIPO_CONTENIDO_CHOICES, 
        initial=Contenido.TEXTO, 
        label='Tipo de Contenido'
    )
    
    texto = forms.CharField(required=False, widget=forms.Textarea, label='Texto')
    imagen_url = forms.URLField(required=False, label='URL de la Imagen')
    imagen_archivo = forms.ImageField(required=False, label='Imagen desde Archivo')
    video_url = forms.URLField(required=False, label='URL del Video')
    video_archivo = forms.FileField(required=False, label='Video desde Archivo')
    ruta = forms.FileField(required=False, label='Archivo')

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = '__all__'
        exclude = ('usuario',)

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = '__all__'


