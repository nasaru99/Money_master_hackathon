# Generated by Django 4.2.4 on 2023-09-12 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0006_comentario_comentario_padre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tokenverificacioncorreo',
            old_name='usuario',
            new_name='user',
        ),
    ]
