# Generated by Django 3.1.7 on 2022-10-31 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico')),
                ('bio', models.TextField(blank=True, max_length=255, verbose_name='Biografía')),
                ('nombres', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellidos')),
                ('imagen', models.ImageField(blank=True, default='a', null=True, upload_to='perfil', verbose_name='Imagen de Perfil')),
                ('provincia', models.CharField(max_length=100, verbose_name='Provincias')),
                ('phone_number', models.CharField(blank=True, max_length=8, verbose_name='Número de teléfono')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('token', models.UUIDField(blank=True, editable=False, null=True)),
                ('new', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]