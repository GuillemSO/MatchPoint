# Generated by Django 5.1.7 on 2025-04-03 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_rename_clubs_club'),
        ('invitaciones', '0001_initial'),
        ('partidos', '0002_rename_partidos_partido'),
        ('resultados', '0002_rename_resultados_resultado'),
        ('tipo_usuario', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usuarios',
            new_name='Usuario',
        ),
    ]
