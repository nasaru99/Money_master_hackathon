# Django built-in imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.contrib import messages  # Importa el sistema de mensajes
from django.core.mail import send_mail  # Importa la función send_mail
from django.template.loader import render_to_string  # Importa la función render_to_string
from django.contrib.sites.shortcuts import get_current_site  # Importa la función get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Pago, Curso
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Amistad
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Amistad
from django.db.models import Q

# Local models
from .models import (
    Curso, Leccion, InscripcionCurso, ProgresoLeccion, MensajePrivado, GrupoChat, Amigo, Amistad,
    TokenVerificacionCorreo, PerfilUsuario, Rol, Permiso, RolPermiso, TipoSuscripcion, Suscripcion,
    TipoPublicacion, Categoria, Etiqueta, Publicacion, Contenido, Comentario, UsuarioGrupo, TipoMensaje,
    EstadoLectura, Pago, RespuestaUsuario, Pregunta, Respuesta
)

# Local forms
from .forms import (
    CursoForm, LeccionForm, CustomUserCreationForm, PerfilUsuarioForm, TokenVerificacionCorreoForm,
    PublicacionForm, LoginForm, ContenidoForm
)

# Other imports
from functools import wraps
import datetime
import uuid
from .services import search_youtube

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

from django.shortcuts import render
from django.db.models import Q
from .models import GrupoChat, Contenido, Publicacion, DetallePerfilUsuario, PerfilUsuario, Curso, Leccion


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
    return render(request, 'inicio.html')

@login_required
def index_contenido(request):
     # Todos los cursos
    cursos = Curso.objects.all()
    # Cursos en progreso del usuario actual
    inscripciones_en_progreso = InscripcionCurso.objects.filter(usuario=request.user, completado=False)
    # Cursos en la lista de deseos del usuario actual
    usuario = request.user
    amigos = Amistad.objects.filter(
        (Q(usuario1=usuario) | Q(usuario2=usuario)) & 
        Q(es_aceptada=True))
    lista_amigos = [amigo.usuario1 if amigo.usuario2 == usuario else amigo.usuario2 for amigo in amigos]
    
    # Obtener las publicaciones del usuario actual y de sus amigos
    publicaciones = Publicacion.objects.filter(
        Q(usuario=usuario) | 
        Q(usuario__in=lista_amigos)
    ).order_by('-fecha_publicacion')

    context = {
        'cursos': cursos,
        'inscripciones_en_progreso': inscripciones_en_progreso,
        'publicaciones': publicaciones,
    }
    return render(request, 'contenido/inicio.html', context)


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

    # Verificar si el usuario ha respondido a todas las preguntas de la lección
    preguntas = Pregunta.objects.filter(leccion=leccion)
    respuestas_usuario = RespuestaUsuario.objects.filter(usuario=request.user, pregunta__in=preguntas)

    # Si el usuario no ha respondido a todas las preguntas o ha respondido incorrectamente, redirigirlo a la página de preguntas

    context = {
        'leccion': leccion,
        'contenido': contenido
    }
    return render(request, 'contenido/contenido_leccion.html', context)


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
from django.views.decorators.http import require_POST
@login_required
@require_POST  # Asegúrate de que sólo se aceptan solicitudes POST
def enviar_solicitud_amistad(request, username):
    print("usuario",username)
    usuario2 = get_object_or_404(User, username=username)
    if Amistad.objects.filter(usuario1=request.user, usuario2=usuario2).exists():
        messages.error(request, 'Ya has enviado una solicitud de amistad a este usuario.')
    else:
        Amistad.objects.create(usuario1=request.user, usuario2=usuario2)
        messages.success(request, 'Solicitud de amistad enviada.')
    return redirect('perfil')


@login_required
def aceptar_solicitud_amistad(request, solicitud_id):
    solicitud = get_object_or_404(Amistad, pk=solicitud_id)
    if solicitud.usuario2 == request.user and not solicitud.es_aceptada:
        solicitud.es_aceptada = True
        solicitud.save()
        messages.success(request, f'Ahora eres amigo de {solicitud.usuario1.username}.')
    else:
        messages.error(request, 'No puedes aceptar esta solicitud.')
    return redirect('perfil')




@method_decorator(login_required, name='dispatch')
class PagoCursoView(View):
    template_name = 'contenido/pagar_curso.html'

    def get(self, request, curso_id, *args, **kwargs):
        curso = get_object_or_404(Curso, id=curso_id)
        return render(request, self.template_name, {'curso': curso})

    def post(self, request, curso_id, *args, **kwargs):
        curso = get_object_or_404(Curso, id=curso_id)
        Pago.objects.create(
            curso=curso,
            usuario=request.user,
            monto=curso.precio,
            metodo_pago='Simulado',
            estado='Completado',
            descripcion=f'Pago de {curso.titulo}'
        )
        return JsonResponse({'success': True, 'message': 'Pago realizado con éxito'})

@login_required
def PagoExitosoView(request):
    return render(request, 'contenido/pago_exitoso.html')


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


@login_required
def perfil_usuario(request, username):

    username=username
    perfil = get_object_or_404(PerfilUsuario, usuario__username=username)
    inscripciones = InscripcionCurso.objects.filter(usuario=perfil.usuario)
    publicaciones = Publicacion.objects.filter(usuario=perfil.usuario)
    amigos = Amigo.objects.filter(usuario1=perfil.usuario) | Amigo.objects.filter(usuario2=perfil.usuario)
    grupos = GrupoChat.objects.filter(usuariogrupo__usuario=perfil.usuario)
    usuario_actual = request.user
    ya_son_amigos = Amistad.objects.filter(
        (Q(usuario1=usuario_actual) | Q(usuario2=usuario_actual)) & 
        (Q(usuario1=perfil.usuario) | Q(usuario2=perfil.usuario)) & 
        Q(es_aceptada=True)
    ).exists()
    context = {
        'ya_son_amigos': ya_son_amigos,
        'username': username,
        'perfil': perfil,
        'inscripciones': inscripciones,
        'publicaciones': publicaciones,
        'amigos': amigos,
        'grupos': grupos,
    }
    return render(request, 'perfil/perfil.html', context)

def user_login(request):
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
    print("comienza")
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES)
        print("comienza primer if")

        if user_form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            user = user_form.save()
            print("comienzasegundo if")
            # Guardar el perfil de usuario
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            detalle_perfil = perfil.detalle
            print("termina crear perfil")

            # Crea un token de verificación de correo
            token = TokenVerificacionCorreo.objects.create(user=user)
            user.is_active = False  # Desactiva el usuario hasta que verifique su correo
            user.save()  # Guarda el estado inactivo del usuario

            # Prepara y envía el correo electrónico de verificación
            mail_subject = 'Activa tu cuenta en HotelHub'
            message = render_to_string('crear_user/activate_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'token': token.token,
            })
            send_mail(mail_subject, message, 'tu_email@gmail.com', [user.email])

            # Redirige al usuario a la página de verificación de correo enviado
            return redirect('email_verification_sent')
        else:
            print("Errores del formulario user: ", user_form.errors)
            print("Errores del formulario perfil: ", perfil_form.errors)
            messages.error(request, 'Hubo un error en el formulario. Por favor, inténtalo de nuevo.')  # Mensaje de error
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
    perfil = PerfilUsuario.objects.get(usuario=usuario)

    inscripciones = InscripcionCurso.objects.filter(usuario=perfil.usuario)

    cursos_creados = Curso.objects.filter(instructor=usuario)
 
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
    amigos = Amistad.objects.filter(
        (Q(usuario1=usuario) | Q(usuario2=usuario)) & 
        Q(es_aceptada=True))
    solicitudes = Amistad.objects.filter(
        (Q(usuario1=usuario) | Q(usuario2=usuario)) & 
        Q(es_aceptada=False))
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
        'perfil': perfil,
        'inscripciones': inscripciones,
        'cursos_creados': cursos_creados,


    }

    return render(request, 'perfil/usuario.html', context)

# servicios

def youtube_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = search_youtube(query)
    return render(request, 'servicios/youtube_search.html', {'results': results})
import json
from google.oauth2 import service_account
from .oauth import get_authenticated_service  # Importa la función de autenticación
from django.contrib.auth.decorators import login_required  # Importa el decorador de autenticación

# ...

@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista
def crear_transmision_en_vivo(request):
    if request.method == 'POST':
        # Obtén los datos del formulario enviado por el usuario
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        fecha_inicio = request.POST['fecha_inicio']
        
        try:
            # Ruta al archivo JSON de la cuenta de servicio
            service_account_file = 'C:\\Users\\Asdrual Lezama\\Downloads\\Educacionl_website\\Educacionl_website\\hotel_website\\client_secret_711545168062-uvq9opsk6jol216rhsikbnt3r6rg86jf.apps.googleusercontent.com.json'

            # Carga el archivo JSON
            with open(service_account_file, 'r') as json_file:
                service_account_info = json.load(json_file)

            # Accede a la información dentro de la clave "web"
            web_info = service_account_info.get('web', {})

            # Verifica si los campos necesarios están presentes
            if 'token_uri' in web_info and 'client_email' in web_info:
                # Los campos necesarios están presentes
                token_uri = web_info['token_uri']
                client_email = web_info['client_email'] # Obtén el correo electrónico del usuario autenticado
                print("correo", client_email)
                print("token_uri", token_uri)
                # Actualiza el campo 'client_email' en la información de la cuenta de servicio
                service_account_info['web']['client_email'] = client_email

                # Crea una credencial a partir de la cuenta de servicio
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    target_principal=client_email,
                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
                )
                print("credentials", credentials)
                # Llama a la función para obtener el servicio autenticado
                youtube = get_authenticated_service(credentials)

                # Crea un nuevo evento de transmisión en vivo
                create_request = youtube.liveBroadcasts().insert(
                    part="snippet,status",
                    body={
                        "snippet": {
                            "title": titulo,
                            "description": descripcion,
                            "scheduledStartTime": fecha_inicio
                        },
                        "status": {
                            "privacyStatus": "public"
                        }
                    }
                )
                
                response = create_request.execute()
                
                # ID del evento de transmisión en vivo que creaste en el paso anterior
                live_broadcast_id = response['id']
                transition_request = youtube.liveBroadcasts().transition(
                    broadcastStatus="live",
                    id=live_broadcast_id,
                    part="status"
                )

                transition_request.execute()

                # Redirige al usuario a una página de confirmación o a la página de la transmisión en vivo
                return redirect('transmision_en_vivo_confirmada')
            else:
                # Los campos necesarios faltan en el archivo JSON
                # Verifica el formato del archivo JSON y su contenido
                print("El archivo JSON de la cuenta de servicio no tiene el formato adecuado o falta información.")
        except FileNotFoundError:
            # El archivo JSON no se encontró en la ubicación especificada
            print("El archivo JSON de la cuenta de servicio no se encontró en la ruta especificada.")
    
    # Renderiza el formulario para que el usuario complete los detalles de la transmisión
    return render(request, 'crear_transmision.html')
