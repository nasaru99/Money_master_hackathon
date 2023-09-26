# Generated by Django 4.2.4 on 2023-09-12 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Texto', 'Texto'), ('Imagen', 'Imagen'), ('Video', 'Video'), ('Ruta', 'Ruta')], default='Texto', max_length=10)),
                ('texto', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='media/galeria')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('ruta', models.FileField(blank=True, null=True, upload_to='media/rutas')),
            ],
        ),
        migrations.RemoveField(
            model_name='publicacion',
            name='imagen',
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='contenido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Money.contenido'),
        ),
    ]
