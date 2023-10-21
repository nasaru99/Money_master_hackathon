from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Imagen(models.Model):
    nombre = models.CharField(max_length=200)
    archivo = models.ImageField(upload_to='imagenes/')
    
    def __str__(self):
        return self.nombre
# gestios de cursos
class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Categorías de educación financiera
    CATEGORIAS_CHOICES = [
        ('EconomiaPersonal', 'Economía Personal'),
        ('FundamentosEmprendimiento', 'Fundamentos de Emprendimiento'),
        ('GestionFinancieraEmpresarial', 'Gestión Financiera Empresarial'),
        ('InversionesMercadosFinancieros', 'Inversiones y Mercados Financieros'),
        ('ImpuestosObligacionesLegales', 'Impuestos y Obligaciones Legales'),
        ('TecnologiaFinanzas', 'Tecnología y Finanzas'),
        ('DesarrolloHabilidadesSoft', 'Desarrollo de Habilidades Soft'),
        ('TendenciasActualidadFinanciera', 'Tendencias y Actualidad Financiera'),
    ]
    
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES, default='EconomiaPersonal')
    
    destacado = models.BooleanField(default=False)
    duracion = models.DurationField(null=True, blank=True)  # Duración total del curso
    fecha_creacion = models.DateTimeField(default=timezone.now)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos_creados')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)
    vistas = models.PositiveIntegerField(default=0)
    lecciones_completadas = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.titulo

class Leccion(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(null=True, blank=True)  # Resumen de la lección
    duracion = models.DurationField(null=True, blank=True)  # Duración de la lección
    contenido = models.OneToOneField('Contenido', on_delete=models.CASCADE, related_name='leccion')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    orden = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo

class InscripcionCurso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    completado = models.IntegerField(default=False)
    progreso = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario.username} inscrito en {self.curso.titulo}"

class ProgresoLeccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    fecha_completado = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'leccion')

    def __str__(self):
        return f"{self.usuario.username} completó {self.leccion.titulo}"

class Pregunta(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    texto = models.TextField()
    correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class RespuestaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'pregunta')

    def __str__(self):
        return f"{self.usuario.username} respondió {self.respuesta.texto} a {self.pregunta.texto}"

# Autenticación y verificación
class TokenVerificacionCorreo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Cambiar 'usuario' a 'user'
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

# Usuario y Perfil
class PerfilUsuario(models.Model):
    # Los campos que ya proporcionaste
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfil_usuarios/', null=True, blank=True)
    foto_portada = models.ImageField(upload_to='fotos_portada_usuarios/', null=True, blank=True)
    biografia = models.TextField(max_length=500, null=True, blank=True)
    rol_trabajo = models.IntegerField(null=True, blank=True)
    nivel_educativo = models.CharField(
        max_length=100, 
        choices=[('principiante', 'Principiante'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')], 
        default='principiante'
    )
    fecha_inicio_suscripcion = models.DateField(null=True, blank=True)
    fecha_fin_suscripcion = models.DateField(null=True, blank=True)
    
    # Nuevos campos inspirados en Facebook y YouTube
    enlace_facebook = models.URLField(max_length=500, null=True, blank=True)
    enlace_youtube = models.URLField(max_length=500, null=True, blank=True)
    numero_seguidores = models.PositiveIntegerField(default=0)
    numero_videos_publicados = models.PositiveIntegerField(default=0)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=10, 
        choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')],
        null=True, blank=True
    )
    lista_amigos_visible = models.BooleanField(default=True) 

    # Nuevos campos para número de teléfono y código de país
    codigo_pais = models.CharField(max_length=10, null=True, blank=True)
    numero_telefono = models.CharField(max_length=15, null=True, blank=True)
    token_acceso_youtube = models.TextField(blank=True, null=True)
    token_actualizacion_youtube = models.TextField(blank=True, null=True)
    id_canal = models.CharField(max_length=255, blank=True, null=True)
    @property
    def esta_suscrito(self):
        if self.fecha_fin_suscripcion:
            return self.fecha_fin_suscripcion > timezone.now().date()
        return False

    def __str__(self):
        return self.usuario.username

class DetallePerfilUsuario(models.Model):
    perfil = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE, related_name='detalle')
    trabajos = models.TextField(null=True, blank=True)  # Puedes considerar usar un modelo separado para trabajos si necesitas más detalles
    estudios = models.TextField(null=True, blank=True)  # Lo mismo para estudios
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    enlace_facebook = models.URLField(max_length=500, null=True, blank=True)
    enlace_instagram = models.URLField(max_length=500, null=True, blank=True)
    enlace_youtube = models.URLField(max_length=500, null=True, blank=True)
    enlace_otras = models.URLField(max_length=500, null=True, blank=True)  # Puedes considerar usar un modelo separado para múltiples enlaces

    def __str__(self):
        return f"Detalle de {self.perfil.usuario.username}"

# Roles y Permisos
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Permiso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    roles = models.ManyToManyField(Rol, through='RolPermiso')

    def __str__(self):
        return self.nombre

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)


# Gestión de Suscripciones
class TipoSuscripcion(models.Model):
    creador = models.ForeignKey(User, related_name='suscripciones_creadas', on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(null=True, blank=True,max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField(null=True, blank=True, help_text="Duración de la suscripción en días.")
    es_recurrente = models.BooleanField(default=True, help_text="Indica si la suscripción se renueva automáticamente.")
    contenido_o_privilegios = models.TextField(null=True, blank=True, help_text="Descripción de lo que el suscriptor obtendrá con esta suscripción.")
    esta_aprobada = models.BooleanField(null=True, blank=True, default=False, help_text="Indica si esta suscripción ha sido aprobada para ser ofrecida a otros usuarios.")

    def __str__(self):
        return self.nombre

class Suscripcion(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('expirado', 'Expirado'),
        ('cancelado', 'Cancelado')
    )

    tipo = models.ForeignKey(TipoSuscripcion, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    suscriptor = models.ForeignKey(User, related_name='suscripciones', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    @property
    def esta_activa(self):
        """ Verifica si la suscripción está activa basándose en las fechas y el estado. """
        return self.estado == 'activo' and self.fecha_fin > timezone.now()

    def __str__(self):
        return f"{self.tipo.nombre} - {self.suscriptor.username}"
# Contenido e Interacción

class TipoPublicacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)


class Contenido(models.Model):
    TEXTO = 'Texto'
    IMAGEN_URL = 'Imagen URL'
    IMAGEN_ARCHIVO = 'Imagen Archivo'  # Nueva opción para imagen desde archivo
    VIDEO_URL = 'Video URL'
    VIDEO_ARCHIVO = 'Video Archivo'  # Nueva opción para video desde archivo
    RUTA = 'Ruta'
    OTRO = 'Otro'

    TIPO_CONTENIDO_CHOICES = [
        (TEXTO, 'Texto'),
        (IMAGEN_URL, 'Imagen URL'),
        (IMAGEN_ARCHIVO, 'Imagen Archivo'),  # Agregamos una opción para imagen desde archivo
        (VIDEO_URL, 'Video URL'),
        (VIDEO_ARCHIVO, 'Video Archivo'),  # Agregamos una opción para video desde archivo
        (RUTA, 'Ruta'),
        (OTRO, 'Otro'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CONTENIDO_CHOICES, default=TEXTO)
    texto = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    imagen_archivo = models.ImageField(upload_to='media/galeria', blank=True, null=True)  # Campo para imágenes desde archivo
    video_url = models.URLField(blank=True, null=True)
    video_archivo = models.FileField(upload_to='media/videos', blank=True, null=True)  # Campo para videos desde archivo
    ruta = models.FileField(upload_to='media/rutas', blank=True, null=True)

    def __str__(self):
        return self.tipo

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_publicacion = models.CharField(max_length=100, choices=[('ARTICULO', 'Artículo'), ('VIDEO', 'Video'), ('PODCAST', 'Podcast')], default='ARTICULO')
    miniatura = models.ImageField(upload_to='miniaturas/', null=True, blank=True)  # Imagen de vista previa
    contenidos = models.ManyToManyField(Contenido)
    suscripcion_requerida = models.ForeignKey(TipoSuscripcion, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    visibilidad = models.CharField(max_length=20, choices=[('Publico', 'Público'), ('Privado', 'Privado'), ('SoloAmigos', 'Solo Amigos'), ('Suscriptores', 'Solo Suscriptores')], default='Publico')
    estado = models.CharField(max_length=15, choices=[('Borrador', 'Borrador'), ('Publicado', 'Publicado'), ('Archivado', 'Archivado')])
    categorias = models.ManyToManyField(Categoria)
    etiquetas = models.ManyToManyField(Etiqueta)
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")
    receptor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='publicaciones_recibidas')

    def __str__(self):
        return self.titulo 

class Comentario(models.Model):
    texto = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=1, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def es_respuesta(self):
        return True if self.comentario_padre else False


# Chat y Mensajes
class GrupoChat(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)
    foto_grupo = models.ImageField(upload_to='fotos_grupo/', null=True, blank=True)
    enlace_invitacion = models.URLField(max_length=500, null=True, blank=True)
    mensaje_anclado = models.ForeignKey('MensajePrivado', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupo_anclado')

class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoChat, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

class TipoMensaje(models.Model):
    descripcion = models.CharField(max_length=50)

class MensajePrivado(models.Model):
    grupo = models.ForeignKey(GrupoChat, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.ForeignKey(TipoMensaje, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_mensaje = models.DateTimeField(auto_now_add=True)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emisor')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receptor')

class EstadoLectura(models.Model):
    mensaje = models.ForeignKey(MensajePrivado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_lectura = models.DateTimeField(null=True)

class Amigo(models.Model):
    usuario1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_usuario1')
    usuario2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_usuario2')
    fecha_amistad = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')

    def __str__(self):
        return f"{self.usuario1.username} y {self.usuario2.username}"


# Gestión de Pagos
class Pago(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50)
    estado = models.CharField(max_length=15, choices=[('Pendiente', 'Pendiente'), ('Completado', 'Completado'), ('Rechazado', 'Rechazado')], default='Pendiente')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class CursoComprado(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)

class Amistad(models.Model):
    usuario1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amistades_iniciadas')
    usuario2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amistades_recibidas')
    fecha_amistad = models.DateTimeField(auto_now_add=True)
    es_aceptada = models.BooleanField(default=False)  # Para manejar solicitudes de amistad pendientes

# Gestión de youtube

class TransmisionEnVivo(models.Model):
    perfil_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    id_transmision_youtube = models.CharField(max_length=255)  # ID de la transmisión en YouTube
    id_stream_youtube = models.CharField(max_length=255)  # ID del stream asociado en YouTube
    hora_inicio = models.DateTimeField(null=True, blank=True)
    hora_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=[
        ('proxima', 'Próxima'),
        ('en_vivo', 'En Vivo'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class AnalisisTransmision(models.Model):
    transmision = models.OneToOneField(TransmisionEnVivo, on_delete=models.CASCADE)
    total_espectadores = models.PositiveIntegerField(default=0)
    maximo_espectadores = models.PositiveIntegerField(default=0)
    tiempo_visionado_promedio = models.PositiveIntegerField(default=0)  # En segundos
    # Otros campos relacionados con las estadísticas de la transmisión.
