# Generated by Django 4.2.4 on 2023-09-14 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0010_curso_leccion_alter_publicacion_categorias_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenido',
            name='leccion',
        ),
        migrations.AlterField(
            model_name='leccion',
            name='contenido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leccion', to='Money.contenido'),
        ),
    ]
