# Generated by Django 4.2.4 on 2023-09-12 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0005_remove_publicacion_dislikes_publicacion_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='comentario_padre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Money.comentario'),
        ),
    ]
