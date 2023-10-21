from django.contrib import admin
from .models import (
    Curso, Leccion, InscripcionCurso, ProgresoLeccion, TokenVerificacionCorreo, PerfilUsuario,
    Rol, Permiso, RolPermiso, TipoSuscripcion, Suscripcion, TipoPublicacion, Categoria, Etiqueta,
    Contenido, Publicacion, Comentario, GrupoChat, UsuarioGrupo, TipoMensaje, MensajePrivado,
    EstadoLectura, Pago, Amigo, Amistad,DetallePerfilUsuario
)
from .models import Imagen


from .models import Pregunta, Respuesta, RespuestaUsuario
class ImagenAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'archivo']
    search_fields = ['nombre']

admin.site.register(Imagen, ImagenAdmin)
class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 3  # Por defecto, muestra 3 campos para respuestas
    fields = ['texto', 'correcta']

class PreguntaAdmin(admin.ModelAdmin):
    fields = ['leccion', 'texto']
    inlines = [RespuestaInline]

class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pregunta', 'respuesta', 'fecha_respuesta']
    list_filter = ['usuario', 'pregunta']
    search_fields = ['usuario__username', 'pregunta__texto', 'respuesta__texto']

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)
admin.site.register(DetallePerfilUsuario)
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_creacion', 'instructor']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden']

@admin.register(InscripcionCurso)
class InscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'curso', 'fecha_inscripcion', 'completado']

@admin.register(ProgresoLeccion)
class ProgresoLeccionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'leccion', 'fecha_completado', 'completado']

@admin.register(TokenVerificacionCorreo)
class TokenVerificacionCorreoAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'fecha_creacion']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol_trabajo', 'nivel_educativo', 'esta_suscrito']

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ['rol', 'permiso']

@admin.register(TipoSuscripcion)
class TipoSuscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'duracion_dias', 'es_recurrente']

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'fecha_inicio', 'fecha_fin', 'suscriptor', 'estado']

@admin.register(TipoPublicacion)
class TipoPublicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'id', 'texto', 'imagen_url', 'video_url', 'ruta')
    list_filter = ('tipo',)
    search_fields = ('texto', 'imagen_url', 'video_url', 'ruta')
    list_per_page = 20

    fieldsets = (
        ('Información del Contenido', {
            'fields': ('tipo', 'texto', 'imagen_url', 'imagen_archivo', 'video_url', 'video_archivo', 'ruta'),
        }),
    )

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_publicacion', 'usuario', 'visibilidad', 'estado']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['texto', 'fecha_comentario', 'usuario', 'publicacion']

@admin.register(GrupoChat)
class GrupoChatAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']

@admin.register(UsuarioGrupo)
class UsuarioGrupoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'grupo', 'fecha_ingreso']

@admin.register(TipoMensaje)
class TipoMensajeAdmin(admin.ModelAdmin):
    list_display = ['descripcion']

@admin.register(MensajePrivado)
class MensajePrivadoAdmin(admin.ModelAdmin):
    list_display = ['grupo', 'tipo', 'texto', 'fecha_mensaje', 'emisor', 'receptor']

@admin.register(EstadoLectura)
class EstadoLecturaAdmin(admin.ModelAdmin):
    list_display = ['mensaje', 'usuario', 'fecha_lectura']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['monto', 'fecha_pago', 'metodo_pago', 'usuario']

@admin.register(Amigo)
class AmigoAdmin(admin.ModelAdmin):
    list_display = ('usuario1', 'usuario2', 'fecha_amistad')

@admin.register(Amistad)
class AmistadAdmin(admin.ModelAdmin):
    list_display = ['usuario1', 'usuario2', 'fecha_amistad', 'es_aceptada']
