# Generated by Django 4.2.4 on 2023-10-11 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0022_alter_perfilusuario_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='curso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Money.curso'),
            preserve_default=False,
        ),
    ]