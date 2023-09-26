# Generated by Django 4.2.4 on 2023-09-21 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Money', '0017_perfilusuario_codigo_pais_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='vistas',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='curso',
            name='categoria',
            field=models.CharField(choices=[('EconomiaPersonal', 'Economía Personal'), ('FundamentosEmprendimiento', 'Fundamentos de Emprendimiento'), ('GestionFinancieraEmpresarial', 'Gestión Financiera Empresarial'), ('InversionesMercadosFinancieros', 'Inversiones y Mercados Financieros'), ('ImpuestosObligacionesLegales', 'Impuestos y Obligaciones Legales'), ('TecnologiaFinanzas', 'Tecnología y Finanzas'), ('DesarrolloHabilidadesSoft', 'Desarrollo de Habilidades Soft'), ('TendenciasActualidadFinanciera', 'Tendencias y Actualidad Financiera')], default='EconomiaPersonal', max_length=100),
        ),
    ]
