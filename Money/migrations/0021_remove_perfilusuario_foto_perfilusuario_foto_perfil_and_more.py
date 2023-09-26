# Generated by Django 4.2.4 on 2023-09-21 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0020_pregunta_respuesta_respuestausuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilusuario',
            name='foto',
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_perfil_usuarios/'),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='foto_portada',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_portada_usuarios/'),
        ),
        migrations.CreateModel(
            name='DetallePerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabajos', models.TextField(blank=True, null=True)),
                ('estudios', models.TextField(blank=True, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True)),
                ('enlace_facebook', models.URLField(blank=True, max_length=500, null=True)),
                ('enlace_instagram', models.URLField(blank=True, max_length=500, null=True)),
                ('enlace_youtube', models.URLField(blank=True, max_length=500, null=True)),
                ('enlace_otras', models.URLField(blank=True, max_length=500, null=True)),
                ('perfil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detalle', to='Money.perfilusuario')),
            ],
        ),
    ]
