from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from functools import wraps
from datetime import timedelta
from .models import Curso, Leccion, InscripcionCurso, ProgresoLeccion
from django.shortcuts import render, redirect, get_object_or_404
from .models import MensajePrivado, GrupoChat
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Amigo,Amistad
from django.shortcuts import render
from .services import search_youtube
import datetime
from django.shortcuts import render, redirect
from .models import Curso, InscripcionCurso, ProgresoLeccion
from .forms import CursoForm, LeccionForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PerfilUsuarioForm
from django.contrib.auth import login

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import TokenVerificacionCorreo, PerfilUsuario
# ...
from .forms import (CustomUserCreationForm, TokenVerificacionCorreoForm, PublicacionForm, 
                    LoginForm, ContenidoForm)
from .models import (TokenVerificacionCorreo, PerfilUsuario, Rol, Permiso, RolPermiso,
                     TipoSuscripcion, Suscripcion, TipoPublicacion, Categoria, Etiqueta, Publicacion, Contenido,
                     Comentario, GrupoChat, UsuarioGrupo, TipoMensaje, MensajePrivado, EstadoLectura, Pago,RespuestaUsuario,Pregunta,Respuesta)
import uuid
from .forms import CustomUserCreationForm

from django.shortcuts import render
from django.db.models import Q  # Agrega esta línea para importar la clase Q
from .models import GrupoChat, Amigo, MensajePrivado
from django.shortcuts import render, get_object_or_404

def trabajador_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        profile = PerfilUsuario.objects.get(user=request.user)
        if profile.trabajador == 1:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No estes jodiendo no eres trabajador.")
    return wrap

# Inicio

def buscar(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        # Búsqueda en distintos modelos
        grupos = GrupoChat.objects.filter(nombre__icontains=query)
        contenidos = Contenido.objects.filter(texto__icontains=query)
        publicaciones = Publicacion.objects.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
        perfiles = PerfilUsuario.objects.filter(usuario__username__icontains=query)
        cursos = Curso.objects.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
        lecciones = Leccion.objects.filter(titulo__icontains=query)

        # Agregar resultados a la lista
        resultados.extend(grupos)
        resultados.extend(contenidos)
        resultados.extend(publicaciones)
        resultados.extend(perfiles)
        resultados.extend(cursos)
        resultados.extend(lecciones)

    return render(request, 'buscar.html', {'resultados': resultados})



def index(request):
    cursos = Curso.objects.all()[:10]  # Obtener los primeros 10 cursos
    comentarios = Comentario.objects.filter(curso__in=cursos)  # Obtener los comentarios de esos cursos

    context = {
        'cursos': cursos,
        'comentarios': comentarios
    }

    return render(request, 'inicio.html', context)
@login_required
def index_contenido(request):
     # Todos los cursos
    cursos = Curso.objects.all()

    # Cursos en progreso del usuario actual
    inscripciones_en_progreso = InscripcionCurso.objects.filter(usuario=request.user, completado=False)

    # Cursos en la lista de deseos del usuario actual
   

    context = {
        'cursos': cursos,
        'inscripciones_en_progreso': inscripciones_en_progreso,
        
    }

    return render(request, 'contenido/inicio.html', context)


def index_contenido_sin_inicio(request):
     # Todos los cursos
    cursos = Curso.objects.all()

    # Cursos en progreso del usuario actual
    
    # Cursos en la lista de deseos del usuario actual
   

    context = {
        'cursos': cursos,
       
        
    }

    return render(request, 'cursos.html', context)


# Gestion de cursos

@login_required
def lecciones_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    lecciones = Leccion.objects.filter(curso=curso)
    context = {
        'curso': curso,
        'lecciones': lecciones
    }
    return render(request, 'contenido/lecciones_curso.html', context)

@login_required
def contenido_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    contenido = leccion.contenido

    # Verificar si el usuario está inscrito en el curso de la lección
    try:
        inscripcion = InscripcionCurso.objects.get(usuario=request.user, curso=leccion.curso)
    except InscripcionCurso.DoesNotExist:
        inscripcion = None

    if not inscripcion:
        # Si el usuario no está inscrito, muestra un mensaje para que realice el pago
        context = {
            'mensaje': 'Para ver el contenido deberá hacer el pago pertinente.'
        }
        return render(request, 'mensaje.html', context)  # Cambia 'ruta_a_template_de_mensaje.html' con la ruta correcta de tu template donde mostrarás el mensaje

    # Verificar si el usuario ha respondido a todas las preguntas de la lección
    preguntas = Pregunta.objects.filter(leccion=leccion)
    respuestas_usuario = RespuestaUsuario.objects.filter(usuario=request.user, pregunta__in=preguntas)

    # Aquí puedes continuar con tu lógica sobre si el usuario ha respondido o no a todas las preguntas...

    context = {
        'leccion': leccion,
        'contenido': contenido
    }
    return render(request, 'contenido/contenido_leccion.html', context)

from django.contrib import messages

@login_required
def responder_preguntas(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    preguntas = leccion.preguntas.all()

    if request.method == "POST":
        respuestas_correctas = 0
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'respuesta_{pregunta.id}')
            if respuesta_id:
                respuesta_seleccionada = Respuesta.objects.get(id=respuesta_id)
                if respuesta_seleccionada.correcta:
                    respuestas_correctas += 1
                # Guardar la respuesta del usuario
                respuesta_usuario, created = RespuestaUsuario.objects.get_or_create(
                    usuario=request.user, pregunta=pregunta,
                    defaults={'respuesta': respuesta_seleccionada}
                )
                if not created:
                    respuesta_usuario.respuesta = respuesta_seleccionada
                    respuesta_usuario.save()

        # Verificar si todas las respuestas son correctas
        if respuestas_correctas == preguntas.count():
            messages.success(request, '¡Todas tus respuestas son correctas!')
            return redirect('contenido_leccion', leccion_id=leccion_id)
        else:
            messages.warning(request, 'Algunas respuestas son incorrectas. Por favor, inténtalo de nuevo.')

    context = {
        'leccion': leccion,
        'preguntas': preguntas
    }
    return render(request, 'contenido/responder_preguntas.html', context)

# Gestion de mensajeria

@login_required
def enviar_mensaje(request):
    mensaje = None
    receptor = request.user
    tipo_mensaje = TipoMensaje.objects.get(id=1)
    grupo = None  # Inicializa grupo con un valor predeterminado

    if request.method == 'POST':
        mensaje_texto = request.POST.get('mensaje')
        receptor_id = request.POST.get('receptor_id')
        grupo_id = request.POST.get('grupo_id')
        
        if receptor_id:
            receptor = User.objects.get(pk=receptor_id)
        
        if grupo_id:
            grupo = GrupoChat.objects.get(pk=grupo_id)
        
        mensaje = MensajePrivado(texto=mensaje_texto, emisor=request.user, receptor=receptor, tipo=tipo_mensaje, grupo=grupo)
        mensaje.save()

    return redirect('perfil')


@login_required
def responder_comentario(request):
    if request.method == "POST":
        texto_respuesta = request.POST.get("respuesta")
        comentario_id = request.POST.get("comentario_id")
        comentario = Comentario.objects.get(id=comentario_id)
        Comentario.objects.create(texto=texto_respuesta, usuario=request.user, publicacion=comentario.publicacion, comentario_padre=comentario)
        return redirect('index_contenido')

@login_required
def dar_like(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    # Si el usuario ya ha dado "me gusta", lo removemos. De lo contrario, lo añadimos.
    if request.user in publicacion.likes.all():
        publicacion.likes.remove(request.user)
    else:
        publicacion.likes.add(request.user)

    return redirect('index_contenido')  # Reemplaza con el nombre de tu URL para mostrar publicaciones

@login_required
def dar_dislike(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    # Si el usuario ya ha dado "dislike", lo removemos. De lo contrario, lo añadimos.
    if request.user in publicacion.dislikes.all():
        publicacion.dislikes.remove(request.user)
    else:
        publicacion.dislikes.add(request.user)

    return redirect('index_contenido')  # Reemplaza con el nombre de tu URL para mostrar publicaciones


@login_required
def comentar_publicacion(request):
    if request.method == "POST":
        texto_comentario = request.POST.get("comentario")
        publicacion_id = request.POST.get("publicacion_id")
        publicacion = Publicacion.objects.get(id=publicacion_id)
        Comentario.objects.create(texto=texto_comentario, usuario=request.user, publicacion=publicacion)
        return redirect('index_contenido')




# Gestion de contenido

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            return redirect('nombre_de_la_url_a_la_que_quieres_redirigir')
    else:
        form = PublicacionForm()
    return render(request, 'crear_publicacion.html', {'form': form})

@login_required
def subir_documento(request, publicacion_id=None):
    if publicacion_id:
        try:
            publicacion = Publicacion.objects.get(pk=publicacion_id)
        except Publicacion.DoesNotExist:
            # Puedes redirigir a una página de error o mostrar un mensaje.
            return HttpResponse("La publicación no existe.")
    else:
        publicacion = None  # Establece esto si deseas crear una nueva publicación en lugar de editar una existente.

    if request.method == 'POST':
        if publicacion:  # Si estamos editando una publicación existente.
            form = PublicacionForm(request.POST, instance=publicacion)
        else:  # Si estamos creando una nueva publicación.
            form = PublicacionForm(request.POST)

        if form.is_valid():
            publicacion = form.save(commit=False)
            if not publicacion_id:
                publicacion.usuario = request.user  # Establecer el usuario solo si es una nueva publicación.
            publicacion.save()
            form.save_m2m()  # Guardar relaciones ManyToMany
            return redirect('index_contenido')

    else:
        if publicacion:
            form = PublicacionForm(instance=publicacion)
        else:
            form = PublicacionForm()

    context = {
        'form': form,
        'publicacion': publicacion  # Esto es opcional, pero puede ser útil si deseas mostrar detalles de la publicación en el template.
    }
    return render(request, 'contenido/subir_documento.html', context)

@login_required
def gestionar_publicacion(request, publicacion_id=None):
    todas_publicaciones = Publicacion.objects.filter(usuario=request.user)
    print("empieza")

    publicacion = None  # Inicializamos la variable

    if publicacion_id:  # Si estás editando o añadiendo a una publicación existente
        publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
        print("empieza con ", publicacion)
        if request.method == 'POST':
            contenido_form = ContenidoForm(request.POST, request.FILES)
            if contenido_form.is_valid():
                contenido = contenido_form.save(commit=False)
                contenido.publicacion = publicacion
                contenido.save()
                print("Contenido guardado:", contenido)
            else:
                print("Error al guardar contenido:", contenido_form.errors)
            pub_form = PublicacionForm(instance=publicacion)
        else:
            pub_form = PublicacionForm(instance=publicacion)
            contenido_form = ContenidoForm()

    else:  # Si estás creando una nueva publicación
        if request.method == 'POST':
            pub_form = PublicacionForm(request.POST)
            if pub_form.is_valid():
                publicacion = pub_form.save(commit=False)
                publicacion.usuario = request.user
                publicacion.save()
                
                # Aquí creamos un contenido predeterminado si no se ha proporcionado
                contenido_form = ContenidoForm(request.POST, request.FILES)
                if not contenido_form.is_valid():
                    Contenido.objects.create(
                        titulo="Contenido predeterminado",
                        descripcion="Este es un contenido predeterminado.",
                        publicacion=publicacion
                    )
                else:
                    contenido = contenido_form.save(commit=False)
                    contenido.publicacion = publicacion
                    contenido.save()
                
                print("Publicación guardada:", publicacion)
            else:
                print("Error al guardar publicación:", pub_form.errors)
            contenido_form = ContenidoForm()
        else:
            pub_form = PublicacionForm()
            contenido_form = ContenidoForm()

    context = {
        'todas_publicaciones': todas_publicaciones,
        'pub_form': pub_form,
        'contenido_form': contenido_form,
        'publicacion': publicacion
    }

    return render(request, 'contenido/gestionar_publicacion.html', context)

@login_required
def iniciar_transmicion(request):
    return render(request, 'contenido/iniciar_transmicion.html')


@login_required
def subir_video(request):
    return render(request, 'contenido/subir_video.html')

@login_required
def crear_leccion(request, curso_id):
    curso = Curso.objects.get(pk=curso_id)

    if request.method == 'POST':
        leccion_form = LeccionForm(request.POST)
        if leccion_form.is_valid():
            # Crea el contenido
            tipo_contenido = leccion_form.cleaned_data.get('tipo_contenido')
            contenido = Contenido(tipo=tipo_contenido)
            
            if tipo_contenido == Contenido.TEXTO:
                contenido.texto = leccion_form.cleaned_data.get('texto')
            elif tipo_contenido == Contenido.IMAGEN_URL:
                contenido.imagen_url = leccion_form.cleaned_data.get('imagen_url')
            elif tipo_contenido == Contenido.IMAGEN_ARCHIVO:
                contenido.imagen_archivo = leccion_form.cleaned_data.get('imagen_archivo')
            elif tipo_contenido == Contenido.VIDEO_URL:
                contenido.video_url = leccion_form.cleaned_data.get('video_url')
            elif tipo_contenido == Contenido.VIDEO_ARCHIVO:
                contenido.video_archivo = leccion_form.cleaned_data.get('video_archivo')
            elif tipo_contenido == Contenido.RUTA:
                contenido.ruta = leccion_form.cleaned_data.get('ruta')
            
            contenido.save()
            
            # Crea la lección y la asocia con el curso y el contenido
            nueva_leccion = leccion_form.save(commit=False)
            nueva_leccion.curso = curso
            nueva_leccion.contenido = contenido
            nueva_leccion.save()
            return redirect('detalle_curso', curso_id=curso_id)
    else:
        leccion_form = LeccionForm()

    return render(request, 'contenido/crear_leccion.html', {'curso': curso, 'leccion_form': leccion_form})

def crear_curso(request):
    if request.method == 'POST':
        curso_form = CursoForm(request.POST, request.FILES)
        if curso_form.is_valid():
            curso = curso_form.save(commit=False)
            curso.instructor = request.user
            curso.save()
            return redirect('detalle_curso', curso_id=curso.id)
    else:
        curso_form = CursoForm()
    return render(request, 'contenido/crear_curso.html', {'curso_form': curso_form})

def detalle_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    lecciones = curso.lecciones.all()
    inscripciones = InscripcionCurso.objects.filter(curso=curso)
    return render(request, 'contenido/detalle_curso.html', {'curso': curso, 'lecciones': lecciones, 'inscripciones': inscripciones})

def inscribir_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    inscripcion, created = InscripcionCurso.objects.get_or_create(usuario=request.user, curso=curso)
    return redirect('detalle_curso', curso_id=curso.id)

def marcar_como_completada(request, leccion_id):
    leccion = Leccion.objects.get(id=leccion_id)
    progreso, created = ProgresoLeccion.objects.get_or_create(usuario=request.user, leccion=leccion)
    progreso.completado = True
    progreso.save()
    return redirect('detalle_curso', curso_id=leccion.curso.id)

# gestion de usuario   


def user_login(request):
    print()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Obtiene el perfil del usuario
                return redirect('/')                
            else:
                # Mensaje de error si la autenticación falla
                form.add_error(None, "Nombre de usuario o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




def registro_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            
            login(request, user)
            
            return redirect('index_contenido')
    else:
        user_form = CustomUserCreationForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'registro.html', {'user_form': user_form, 'perfil_form': perfil_form})


class SignUpView(CreateView):
    model = User  # Especifica el modelo User
    form_class = UserCreationForm  # Usa el formulario de creación de usuario incorporado
    template_name = 'crear_user/crear_usuario.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Procesar los datos del formulario manualmente
        username = self.request.POST.get('username')
        last_name = self.request.POST.get('last_name')
        birthdate = self.request.POST.get('birthdate')
        email = self.request.POST.get('email')
        country_code = self.request.POST.get('country_code')
        phone_number = self.request.POST.get('phone_number')
        gender = self.request.POST.get('gender')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        accept_terms = self.request.POST.get('accept_terms')

        # Crea un nuevo usuario y guárdalo
        user = User.objects.create_user(username=username, last_name=last_name, birthdate=birthdate,
                                        email=email, country_code=country_code,
                                        phone_number=phone_number, gender=gender,
                                        password=password1)
        user.is_active = False
        user.save()

        # Crea un token de verificación de correo
        token = TokenVerificacionCorreo.objects.create(user=user)

        # Crea un perfil de usuario relacionado
        perfil_usuario = PerfilUsuario(usuario=user)
        perfil_usuario.save()

        mail_subject = 'Activa tu cuenta en HotelHub'
        message = render_to_string('crear_user/activate_email.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'token': token.token,
        })
        send_mail(mail_subject, message, 'tu_email@gmail.com', [user.email])

        # Inicia sesión al usuario
        login(self.request, user)

        return redirect('email_verification_sent')



def activate_account(request, token: None):
    try:
        verification_token = TokenVerificacionCorreo.objects.get(token=token)
        # Comprobar si el token ha expirado
        expiration_duration = datetime.timedelta(hours=48)  # 48 horas por ejemplo
        if timezone.now() - verification_token.fecha_creacion > expiration_duration:
            verification_token.delete()  # Eliminar tokens expirados
            return render(request, 'crear_user/activation_expired.html')  # Página de token expirado
        user = verification_token.user
        user.is_active = True
        user.save()
        login(request, user)
        verification_token.delete()
        return redirect('index')
    except TokenVerificacionCorreo.DoesNotExist:
        return render(request, 'crear_user/activation_invalid.html')

def email_verification_sent(request):
    return render(request, 'crear_user/email_verification_sent.html')

def solicitar_recuperacion(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            # Eliminar tokens existentes para el mismo usuario
            TokenVerificacionCorreo.objects.filter(user=user).delete()

            # Generar token y enviar correo
            token = TokenVerificacionCorreo.objects.create(user=user)
            mail_subject = 'Recuperación de contraseña'
            domain = get_current_site(request).domain
            reset_link = f"http://{domain}/resetear-contraseña/{token.token}/"
            message = render_to_string(
                'crear_user/reset_password_email.html',
                {
                    'usuario': user,
                    'reset_link': reset_link,
                }
            )
            send_mail(mail_subject, message, 'tu_email@gmail.com', [user.email])
            return redirect('email_verification_sent')
        else:
            # Mostrar mensaje de error o simplemente redirigir
            return redirect('solicitar_recuperacion')
    return render(request, 'crear_user/solicitar_recuperacion.html')

def resetear_contraseña(request, token):
    token_obj = TokenVerificacionCorreo.objects.filter(token=token).first()
    if not token_obj:
        return render(request, 'crear_user/reset_token_invalid.html')
    
    # Comprobar si el token ha expirado
    expiration_duration = datetime.timedelta(hours=48)  # 48 horas por ejemplo
    if timezone.now() - token_obj.fecha_creacion > expiration_duration:
        token_obj.delete()  # Eliminar tokens expirados
        return render(request, 'crear_user/reset_token_expired.html')  # Página de token expirado

    if request.method == 'POST':
        new_password = request.POST['new_password']
        user = token_obj.user
        user.set_password(new_password)
        user.save()
        token_obj.delete()
        return redirect('login')
    
    return render(request, 'crear_user/resetear_contraseña.html')

from .models import PerfilUsuario, DetallePerfilUsuario, Publicacion
@login_required
def perfil(request):
    
    usuario = request.user
    amigos = Amistad.objects.filter(usuario1=usuario) 
    # Get the user's profile
    perfil_usuario = get_object_or_404(PerfilUsuario, usuario=request.user)
    detalle_perfil = DetallePerfilUsuario.objects.get(perfil=perfil_usuario)  # Cambio aquí

    # Obtener las publicaciones del usuario
    publicaciones = Publicacion.objects.filter(usuario=perfil_usuario.usuario).order_by('-fecha_publicacion')[:5]  # Cambio aquí

    # Get the subscriptions of the user
    suscripciones_usuario = Suscripcion.objects.filter(suscriptor=request.user)

    # Get the subscription types created by the user
    suscripciones_creadas = TipoSuscripcion.objects.filter(creador=request.user)

    # Get the groups the user belongs to
    grupos_usuario = UsuarioGrupo.objects.filter(usuario=request.user)
    # Obtener los amigos del usuario
    usuario = request.user
    amigos = Amistad.objects.filter(Q(usuario1=usuario) | Q(usuario2=usuario))
    grupos = GrupoChat.objects.filter(usuariogrupo__usuario=request.user)
    # Obtener los mensajes del primer grupo (puedes personalizar esta lógica)
    primer_grupo = grupos.first()
    mensajes = MensajePrivado.objects.filter(grupo=primer_grupo)
    mensajes_amigos= MensajePrivado.objects.all()
    
    # Obtener tipos de mensajes para mostrar
    tipos_mensaje = TipoMensaje.objects.all()
    # Combine all the data into the context
    context = {
        'perfil_usuario': perfil_usuario,  # Cambio aquí
        'detalle_perfil': detalle_perfil,
        'publicaciones': publicaciones,
        'amigos': amigos,
        'suscripciones_usuario': suscripciones_usuario,
        'suscripciones_creadas': suscripciones_creadas,
        'grupos_usuario': grupos_usuario,
        'mensajes_amigos': mensajes_amigos,
        'grupos': grupos,
        'amigos': amigos,
        'mensajes': mensajes,
        'tipos_mensaje': tipos_mensaje,

    }

    return render(request, 'perfil/usuario.html', context)

# servicios

def youtube_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = search_youtube(query)
    return render(request, 'servicios/youtube_search.html', {'results': results})

def aprendizaje(request):
    return render(request, 'aprendizaje.html')

def nosotros(request):
    return render(request, 'Nos.html')

def compras(request):
    return render(request, 'compras.html')

def pago(request):
    return render(request, 'pago.html')

def explorador(request):
    return render(request, 'explorador.html')