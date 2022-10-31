
from django.db.models.fields import TimeField
from posts.models import *


def get_everything(request):

    categories= Category.objects.all()
    gen=TIPOS1
    tip=TIPOS2
    articles=Article.objects.all().order_by("-id").filter(public=True)[:8]
    mujer=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Mujeres")[:6]
    hombres=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Hombres")[:6]
    niños=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Niños")[:6]
    unisex=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Unisex")[:6]
    likes=Article.num_likes

    

    return{
        'categories': categories, 
        'gens': gen,
        'tipos': tip ,
        'articles': articles,
        "likes": likes,
        "mujer":mujer,
        "hombre":hombres,
        "niños":niños,
        "unisex":unisex,
    }

