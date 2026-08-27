from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="inicio"),
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("salir/", views.logout_view, name="logout"),
    path("no_permisos/", views.no_permisos, name="no_permisos"),
    path("cambiar_contraseña/", auth_views.PasswordChangeView.as_view(template_name="usuarios/cambiar_contrasenia.html", success_url=reverse_lazy("home")), name="cambiar_contraseña"),
    path("cambiar_contraseña/exito/", auth_views.PasswordChangeDoneView.as_view(template_name="usuarios/cambiar_contrasenia_exito.html"), name="cambiar_contraseña_exito"),

]
