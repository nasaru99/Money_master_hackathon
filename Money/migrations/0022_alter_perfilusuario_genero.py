# Generated by Django 4.2.4 on 2023-10-11 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0021_remove_perfilusuario_foto_perfilusuario_foto_perfil_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='genero',
            field=models.CharField(blank=True, choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Otro', 'Otro')], max_length=10, null=True),
        ),
    ]
