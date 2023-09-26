# Generated by Django 4.2.4 on 2023-09-14 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0012_curso_imagen_curso_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contenido',
            old_name='imagen',
            new_name='imagen_archivo',
        ),
        migrations.AddField(
            model_name='contenido',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contenido',
            name='video_archivo',
            field=models.FileField(blank=True, null=True, upload_to='media/videos'),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='tipo',
            field=models.CharField(choices=[('Texto', 'Texto'), ('Imagen URL', 'Imagen URL'), ('Imagen Archivo', 'Imagen Archivo'), ('Video URL', 'Video URL'), ('Video Archivo', 'Video Archivo'), ('Ruta', 'Ruta'), ('Otro', 'Otro')], default='Texto', max_length=20),
        ),
    ]