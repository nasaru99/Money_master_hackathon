from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import include
urlpatterns = [
    path('buscar/', views.buscar, name='buscar'),
    # Rutas para la página de inicio
    path('registro/', views.registro_view, name='registro'),
    path('', views.index, name='index'),
    path('Contenido/', views.index_contenido, name='index_contenido'),
    path('Contenido/sin_inicio', views.index_contenido_sin_inicio, name='index_contenido_sin_inicio'),
    path('aprendizaje/', views.aprendizaje, name='aprendizaje'),
    path('compras/<int:curso_id>/', views.compras, name='compras'),

   path('pago/<int:curso_id>/', views.pago, name='pago'),

    # Rutas para la gestión de servicios
    path('search/', views.youtube_search, name='youtube_search'),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('explorador', views.explorador, name='explorador'),
    # Rutas para la gestión de usuario
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.user_login, name='login'),
    path('activate/<uuid:token>/', views.activate_account, name='activate_account'),
    path('email-verification-sent/', views.email_verification_sent, name='email_verification_sent'),
    path('solicitar-recuperacion/', views.solicitar_recuperacion, name='solicitar_recuperacion'),
    path('resetear-contraseña/<uuid:token>/', views.resetear_contraseña, name='resetear_contraseña'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rutas para la gestión de contenido
    path('nosotros/', views.nosotros, name='nosotros'),
    path('perfil/', views.perfil, name='perfil'),
    path('contenido/crear_curso/', views.crear_curso, name='crear_curso'),
    path('contenido/crear_leccion/<int:curso_id>/', views.crear_leccion, name='crear_leccion'),
    path('contenido/curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('contenido/curso/<int:curso_id>/lecciones/', views.lecciones_curso, name='lecciones_curso'),
    path('contenido/leccion/<int:leccion_id>/contenido/', views.contenido_leccion, name='contenido_leccion'),
    path('contenido/leccion/<int:leccion_id>/preguntas/', views.responder_preguntas, name='responder_preguntas'),
    path('contenido/curso/<int:curso_id>/inscribir/', views.inscribir_curso, name='inscribir_curso'),
    path('contenido/leccion/<int:leccion_id>/completar/', views.marcar_como_completada, name='marcar_como_completada'),
    path('Contenido/comentar/', views.comentar_publicacion, name='comentar_publicacion'),
    path('contenido/dar_like/<int:publicacion_id>/', views.dar_like, name='dar_like'),
    path('contenido/dar_dislike/<int:publicacion_id>/', views.dar_dislike, name='dar_dislike'),
    path('contenido/responder_comentario/', views.responder_comentario, name='responder_comentario'),
    path('contenido/iniciar_transmicion/', views.iniciar_transmicion, name='iniciar_transmicion'),
    path('contenido/subir_documento/', views.subir_documento, name='subir_documento'),
    path('contenido/subir_video/', views.subir_video, name='subir_video'),
    path('contenido/gestionar_publicacion/', views.gestionar_publicacion, name='gestionar_publicacion'),
    path('contenido/gestionar_publicacion/<int:publicacion_id>/', views.gestionar_publicacion, name='gestionar_publicacion_con_id'),

    # Otras rutas ...
    path('iniciar_oauth2/', views.iniciar_oauth2, name='iniciar_oauth2'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('youtube_auth/', views.oauth2callback, name='youtube_auth'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)