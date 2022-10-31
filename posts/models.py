from django.db import models
from django.db.models.base import Model

from django.db.models.fields.related import ManyToManyField
from django.utils import tree
from ckeditor.fields import RichTextField
from user.models import Usuario



TIPOS2=(
    ('Superior','Superior'),
    ('Inferior','Inferior'),
    ('Ropa interior','Ropa interior'),
    ('Trajes de baño','Trajes de baño'),
    ('Accesorios','Accesorios'),
    ('Cuidado de la piel y maquillaje','Cuidado de la piel y maquillaje'),
    ('Otros', 'Otros'),

)
TIPOS1=(
    ('Mujeres','Mujeres'),
    ('Hombres','Hombres'),
    ('Niños','Niños'),
    ('Unisex','Unisex')
)

verbose_name_plural="Clase"

class Category(models.Model):
    name=models.CharField(max_length=100, verbose_name="Nombre")
    
    
    

    def __str__(self) :
        return f"{self.name}"
    
    class Meta:
        verbose_name="Categoría"
        verbose_name_plural="Categorías"
    

class Article(models.Model):
    titulo=models.CharField(max_length=150, verbose_name='Titulo')
    descripcion=models.CharField(max_length=255 , verbose_name="Descripción")
    public=models.BooleanField(verbose_name="Público", default=True)
    image=models.ImageField(upload_to="articles/", verbose_name="Imagen", null=True, )
    image2=models.ImageField(upload_to="articles/", verbose_name="Imagen", null=True, )
    image3=models.ImageField(upload_to="articles/", verbose_name="Imagen", null=True, )
    user=models.ForeignKey(Usuario, editable=False, verbose_name="Usuario", on_delete=models.CASCADE)
    categories =models.ForeignKey(Category, verbose_name="Categorías", on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True, verbose_name="Creado el")
    talla=models.CharField(max_length=3, verbose_name="Talla", blank=True, default="")
    precio=models.FloatField(verbose_name="Precio")
    stock=models.IntegerField(verbose_name="Inventario", default=1)
    liked=models.ManyToManyField(Usuario, default=None, blank=True, related_name="Liked")
    tipo=models.CharField(max_length=100, choices=TIPOS1)
    clase=models.CharField(max_length=100, choices=TIPOS2)
    destacado=models.BooleanField(verbose_name="Destacados", default=False)

    def __str__(self) :
        return f"{self.titulo}"
    
    
    def num_likes(self):
        return self.liked.all().count()
    
    class Meta:
        verbose_name="Artículo"
        verbose_name_plural="Artículos"


LIKE_CHOICES=(
    ("Like","Like"),
    ("Unlike","Unlike")
)

class Like(models.Model):
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post=models.ForeignKey(Article, on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES, default="Like", max_length=10)

    def __str__(self):
        return str(self.post)
