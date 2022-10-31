from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.files import ImageField
from django.forms.fields import TypedChoiceField
from django.core.validators import RegexValidator


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombres, apellidos, password=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        
        usuario=self.model(username=username, email=self.normalize_email(email), nombres=nombres, apellidos=apellidos)

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, email,  nombres, apellidos, password):
        usuario=self.create_user(email, username=username, nombres=nombres, apellidos=apellidos, password=password)
        usuario.usuario_administrador=True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    username=models.CharField("Nombre de usuario", unique = True, max_length=50)
    email=models.EmailField("Correo electrónico", max_length=254, unique=True)
    bio=models.TextField("Biografía", max_length=255, blank=True)
    nombres=models.CharField("Nombres", max_length=200, blank=True, null=True)
    apellidos=models.CharField("Apellidos", max_length=200, blank=True, null=True)
    imagen=ImageField("Imagen de Perfil", upload_to="perfil", blank=True, null=True, default="a")
    provincia=models.CharField(max_length=100,verbose_name="Provincias")
    phone_number = models.CharField("Número de teléfono",  max_length=8, blank=True)
    usuario_activo=models.BooleanField(default=True)
    usuario_administrador=models.BooleanField(default=False)
    objects=UsuarioManager()
    token=models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    new=models.BooleanField(default=True)


    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email', 'nombres', 'apellidos']

    def __str__(self):
        return f"{self.nombres}, {self.apellidos}"

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
    @property
    def is_active(self):
        return self.usuario_activo


