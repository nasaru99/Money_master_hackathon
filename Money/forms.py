from django import forms
from django.contrib.auth.models import User
from .models import TokenVerificacionCorreo, PerfilUsuario, Publicacion, Comentario, MensajePrivado, Pago
import uuid
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Publicacion, Contenido
from .models import Curso, Leccion


class PerfilUsuarioForm(forms.ModelForm):
    
    # Ya definidos anteriormente:
    foto_perfil = forms.ImageField(
        label='Foto de perfil',
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )
    foto_portada = forms.ImageField(
        label='Foto de portada',
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Breve biografía...'
        }),
        label='Biografía'
    )
    rol_trabajo = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Rol de trabajo'
    )
    nivel_educativo = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Nivel educativo'
    )
    enlace_facebook = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enlace a Facebook'
        }),
        label='Facebook'
    )
    enlace_youtube = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enlace a YouTube'
        }),
        label='YouTube'
    )

    # Añadiendo estilos a los campos restantes:
    fecha_inicio_suscripcion = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha inicio de suscripción'
    )
    fecha_fin_suscripcion = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha fin de suscripción'
    )
    numero_seguidores = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        label='Número de seguidores'
    )
    numero_videos_publicados = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        label='Número de videos publicados'
    )
    ubicacion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ubicación'
        }),
        label='Ubicación'
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de nacimiento'
    )

    genero = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Género'
    )
    lista_amigos_visible = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='¿Lista de amigos visible?'
    )
    codigo_pais = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código del país'
        }),
        label='Código del país'
    )
    numero_telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de teléfono'
        }),
        label='Número de teléfono'
    )

    class Meta:
        model = PerfilUsuario
        fields = [
            'foto_perfil', 'foto_portada', 'biografia', 'rol_trabajo',
            'nivel_educativo', 'fecha_inicio_suscripcion', 'fecha_fin_suscripcion',
            'enlace_facebook', 'enlace_youtube', 'numero_seguidores',
            'numero_videos_publicados', 'ubicacion', 'fecha_nacimiento',
            'genero', 'lista_amigos_visible', 'codigo_pais', 'numero_telefono'
        ]

class TokenVerificacionCorreoForm(forms.ModelForm):
    class Meta:
        model = TokenVerificacionCorreo
        exclude = ['token']
        fields = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'ph-center',
            'placeholder': 'Nombre de usuario',
        }),
        label=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'ph-center',
            'placeholder': 'Contraseña',
        }),
        label=False
    )

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




class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nivel_educativo', 'ubicacion', 'fecha_nacimiento', 'genero', 'codigo_pais', 'numero_telefono']
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


