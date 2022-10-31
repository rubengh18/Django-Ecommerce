# Generated by Django 3.1.7 on 2022-10-31 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150, verbose_name='Titulo')),
                ('descripcion', models.CharField(max_length=255, verbose_name='Descripción')),
                ('public', models.BooleanField(default=True, verbose_name='Público')),
                ('image', models.ImageField(null=True, upload_to='articles/', verbose_name='Imagen')),
                ('image2', models.ImageField(null=True, upload_to='articles/', verbose_name='Imagen')),
                ('image3', models.ImageField(null=True, upload_to='articles/', verbose_name='Imagen')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creado el')),
                ('talla', models.CharField(blank=True, default='', max_length=3, verbose_name='Talla')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('stock', models.IntegerField(default=1, verbose_name='Inventario')),
                ('tipo', models.CharField(choices=[('Mujeres', 'Mujeres'), ('Hombres', 'Hombres'), ('Niños', 'Niños'), ('Unisex', 'Unisex')], max_length=100)),
                ('clase', models.CharField(choices=[('Superior', 'Superior'), ('Inferior', 'Inferior'), ('Ropa interior', 'Ropa interior'), ('Trajes de baño', 'Trajes de baño'), ('Accesorios', 'Accesorios'), ('Cuidado de la piel y maquillaje', 'Cuidado de la piel y maquillaje'), ('Otros', 'Otros')], max_length=100)),
                ('destacado', models.BooleanField(default=False, verbose_name='Destacados')),
            ],
            options={
                'verbose_name': 'Artículo',
                'verbose_name_plural': 'Artículos',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.category', verbose_name='Categorías'),
        ),
        migrations.AddField(
            model_name='article',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='Liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]