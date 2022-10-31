from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from django import http
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.query_utils import Q
from django.forms import forms
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from user.forms import FormularioUsuario, FormularioLogin, ResetPassWordForm,ChangePassWordForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from posts.models import Article, Like
from user.models import Usuario
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from posts.forms import FormArticle, FormEdit
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import smtplib
import uuid
def HomeView(request):
    queryset=request.GET.get("buscar")
    
    if queryset:
        return redirect(f"all-articles/?buscar={queryset}")
    return render(request, "index2.html")

class Login(FormView):
    template_name="login.html"
    form_class=FormularioLogin
    success_url=reverse_lazy("index")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request,*args, **kwargs)
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def RegisterView(request):
    queryset=request.GET.get("buscar")
    if queryset:
        return redirect(f"articles/?buscar={queryset}")
    register_form=FormularioUsuario()
    if request.method=='POST':
        register_form=FormularioUsuario(request.POST)
        
        
        if register_form.is_valid():
            register_form.save()
            return redirect('login')
     
    return render(request, 'register.html',{
        'register_form': register_form
    })        

def ArticleView(request, article_id):
    queryset=request.GET.get("buscar")
    if queryset:
        return redirect(f"articles/?buscar={queryset}")
    article=get_object_or_404(Article, id=article_id)
    return render(request, "article.html",{
        "article": article,
        
    })

@login_required(login_url="login")
def Profile(request, username):
    queryset=request.GET.get("buscar")
    if queryset:
        return redirect(f"all-articles/?buscar={queryset}")
    usuario=get_object_or_404(Usuario, username=username)
    posts=Article.objects.filter(user=usuario.id).order_by("-id").filter(public=True)
    return render(request, "profile.html",{
        "usuario":usuario,
        "posts":posts
    })

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("index")

def AllArticles(request):
    queryset=request.GET.get("buscar")
    posts=Article.objects.filter(public=True).order_by("-id")
    if queryset:
        posts=Article.objects.filter(
            Q(titulo__icontains=queryset)|
            Q(descripcion__icontains=queryset)
        ).distinct()

    

    return render(request,"AllArticles.html", {"posts":posts})

@login_required(login_url="login")
def DarLike(request):
    user = request.user
    
    if request.method == 'POST':
        post_id = request.POST.get('article_id')
        post_obj = Article.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return HttpResponseRedirect(f"/article/{post_id}")


@login_required(login_url="login")
def crearArticulo(request):
    queryset=request.GET.get("buscar")
    if queryset:
        return redirect(f"articles/?buscar={queryset}")
    if request.method == 'POST':
        form = FormArticle(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('index')
    else:
        form = FormArticle()
    
    return render(request,'crearArticulo.html',{'form':form})

@login_required(login_url="login")
def profileEdit(request):
    user=request.user
    def_img=user.imagen
    if request.method == 'POST':
        imagen=request.FILES.get("imagen")
        name=request.POST.get("nombres")
        apellidos=request.POST.get("apellidos")
        bio=request.POST.get("bio")
        username=request.POST.get("username")
        phone=request.POST.get("phone")
        provincia=request.POST.get("provincia")
        email=request.POST.get("email")
        if user.new:
            user.new=False
        user.nombres=name
        user.apellidos=apellidos
        if imagen:
            user.imagen=imagen
        else:
            user.imagen=def_img
        user.bio=bio
        user.phone_number=phone
        user.username=username
        user.provincia=provincia
        user.email=email
        user.save()
        return redirect("profile", request.user.username)
    return render(request, 'profileEdit.html')

def destacados(request):
    des=Article.objects.all().order_by("-created_at").filter(public=True).filter(destacado=True)
    return render (request, 'destacados.html', {"des":des})
def mujeres(request):
    mujeres=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Mujeres")
    return render (request, 'mujeres.html', {"mujeres":mujeres})

def hombres(request):
    hombres=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Hombres")
    return render (request, 'hombres.html', {"hombres":hombres})

def niños(request):
    ninos=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Niños")
    return render (request, 'niños.html', {"ninos":ninos})
def unisex(request):
    unis=Article.objects.all().order_by("-id").filter(public=True).filter(tipo="Unisex")
    return render (request, 'unisex.html',{"unis":unis})

def editArticle(request, article_id):
    article=Article.objects.filter(id=article_id).first()
    form = FormEdit(instance=article)
    if request.user == article.user:

        return render(request, "editar.html", {"form":form, "article":article,})
    else:
        return redirect("index")

def Actualizar(request, article_id):
    articles=Article.objects.get(pk=article_id)
    form=FormEdit(request.POST, request.FILES, instance=articles)
    if form.is_valid():
        form.save()
    return redirect("article", article_id)

def Eliminar(request, article_id):
    articles=Article.objects.get(pk=article_id)
    if request.user==articles.user:
        articles.delete()
    return redirect("index")

def NewPassword(request):
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("login")
    else:
        form=PasswordChangeForm(user=request.user)
        return render(request, "change_password.html", {"form": form})
            

def send_email(mail):
    
        try:
            mailServer=smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to=mail
            mensaje=MIMEMultipart()
            mensaje["From"]=settings.EMAIL_HOST_USER
            mensaje["To"]=email_to
            mensaje["Subject"]="Tienes un correo"
            content=render_to_string("correo.html")
            mensaje.attach(MIMEText(content, "html"))
            mailServer.sendmail(
                settings.EMAIL_HOST_USER,
                email_to,
                mensaje.as_string()
            )
        except Exception as e:
            print(e)

class ResetPasswordView(FormView):
    form_class=ResetPassWordForm
    template_name="change_password.html"
    success_url=reverse_lazy("index")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def send_email_password(self, user):
        data={}
        try:
            URL="dekche.com"

            user.token= uuid.uuid4()
            user.save()

            mailServer=smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to=user.email
            mensaje=MIMEMultipart()
            mensaje["From"]=settings.EMAIL_HOST_USER
            mensaje["To"]=email_to
            mensaje["Subject"]="Reseteo de Contraseña"
            content=render_to_string("correo.html",{
                "user":user,
                "link_resetpwd":"http://{}/change/password/{}".format(URL, str(user.token)),
                "link_home":"http://{}".format(URL)
            })
            mensaje.attach(MIMEText(content, "html"))
            mailServer.sendmail(
                settings.EMAIL_HOST_USER,
                email_to,
                mensaje.as_string()
            )
        except Exception as e:
            data["error"]=str(e)
        return data
            

    def post(self, request, *args, **kwargs):
        data={}
        try:
            form= ResetPassWordForm(request.POST)
            if form.is_valid():
                user=form.get_user()
                
                data=self.send_email_password(user)
            else:
                data["error"]=form.errors
            print(request.POST)
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="Reseteo de Contraseña"
        return context
    

class ChangePasswordView(FormView):
    form_class=ChangePassWordForm
    template_name="changepwd.html"
    success_url=reverse_lazy("index")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) :
        token=self.kwargs["token"]
        if Usuario.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs) 
        return HttpResponseRedirect("/")      

    def post(self, request, *args, **kwargs):
        data={}
        try:
            form=ChangePassWordForm(request.POST)
            if form.is_valid():
                user=Usuario.objects.get(token=self.kwargs["token"])
                user.set_password(request.POST["password"])
                user.token= uuid.uuid4()
                user.save()
            else:
                data["error"]=form.errors
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="Reseteo de Contraseña"
        return context

@login_required(login_url="login")
def Favoritos(request):
    like=Like.objects.all().order_by("-id")
    
    return render(request, 'favoritos.html', {"fav":like})

def Terminos(request):
    return render (request, "terms.html")
    
        