
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from mainapp import views
from django.contrib.auth import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView, name="index"),
    path('register/', views.RegisterView, name="register"),
    path('accounts/login/', views.Login.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:username>/', views.Profile, name="profile"),
    path('article/<int:article_id>', views.ArticleView, name="article"),
    path('like/', views.DarLike, name="dar_like"),
    path('all-articles/', views.AllArticles, name="articles"),
    path('new-article/', views.crearArticulo, name="crear"),
    path('edit-profile/', views.profileEdit, name="editarp"),
    path('category/mujeres', views.mujeres, name="mujeres"),
    path('category/hombres', views.hombres, name="hombres"),
    path('category/niños', views.niños, name="niños"),
    path('category/unisex', views.unisex, name="unisex"),
    path('edit/<int:article_id>', views.editArticle, name="editar"),
    path('actualizar/<int:article_id>', views.Actualizar, name="actualizar"),
    path('eliminar/<int:article_id>', views.Eliminar, name="eliminar"),
    path('new-password/', views.NewPassword, name="nueva_contraseña"),
    path('email/', views.send_email, name="email"),
    path('reset/password', views.ResetPasswordView.as_view(), name="reset_password"),
    path('change/password/<str:token>', views.ChangePasswordView.as_view(), name="change_password"),
    path('favorites/', views.Favoritos, name="favoritos"),
    path('terminos/', views.Terminos, name="terminos"),
    path('destacados', views.destacados, name="destacados"),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




