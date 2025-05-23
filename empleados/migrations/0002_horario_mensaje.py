# Generated by Django 5.1.4 on 2025-05-17 21:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=10)),
                ('entrada', models.TimeField()),
                ('salida', models.TimeField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibidos', to=settings.AUTH_USER_MODEL)),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
