# populate_data.py
import os
import django
from faker import Faker
from django.contrib.auth.models import User
from .models import Roles, Permisos, TipoSuscripcion, Suscripciones, Perfiles, RolesPermisos, Publicaciones, Comentarios, GruposChat, UsuariosGrupos, TiposMensaje, MensajesPrivados, EstadosLectura, Pagos

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tu_proyecto.settings")
django.setup()

# Inicializar Faker
fake = Faker()

# Función para crear datos falsos
def create_fake_data():
    # Crear roles y permisos falsos
    for _ in range(10):
        Roles.objects.create(NombreRol=fake.word())
        Permisos.objects.create(NombrePermiso=fake.word(), Descripcion=fake.sentence())

    # Crear tipos de suscripción y suscripciones falsos
    for _ in range(5):
        TipoSuscripcion.objects.create(Nombre=fake.word(), Descripcion=fake.sentence(), Precio=fake.random_int(1, 100))

    for _ in range(20):
        TipoID = TipoSuscripcion.objects.order_by("?").first()
        Suscripciones.objects.create(Tipo=TipoID, FechaInicio=fake.date_time_this_decade(), FechaFin=fake.date_time_this_decade())

    # Crear usuarios falsos
    for _ in range(50):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, email=email, password=password)

        # Crear perfiles falsos
        Perfiles.objects.create(FotoPerfil=fake.image_url(), Descripcion=fake.text(), user=user)

        # Asignar roles y permisos falsos a usuarios
        roles = Roles.objects.order_by("?")[:fake.random_int(1, 3)]
        for rol in roles:
            user.roles.add(rol)

        permisos = Permisos.objects.order_by("?")[:fake.random_int(1, 5)]
        for permiso in permisos:
            user.permisos.add(permiso)

    # Crear publicaciones y comentarios falsos
    for _ in range(100):
        user = User.objects.order_by("?").first()
        Publicaciones.objects.create(TipoPublicacion=fake.word(), Contenido=fake.text(), user=user)

    for _ in range(200):
        user = User.objects.order_by("?").first()
        publicacion = Publicaciones.objects.order_by("?").first()
        Comentarios.objects.create(Texto=fake.text(), user=user, Publicacion=publicacion)

    # ... Continúa creando datos falsos para las otras tablas

if __name__ == "__main__":
    create_fake_data()
