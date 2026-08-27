from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Vista para la página de inicio, que muestra diferentes opciones según el rol del usuario (inspector, encargado de playón, admin del sistema, juez).
@login_required
def home(request):
    grupos_usuario = set(request.user.groups.values_list("name", flat=True))

    context = {
        "es_admin_sistema": "ADMINISTRADOR" in grupos_usuario,
        "es_administrativo": "ADMINISTRATIVO" in grupos_usuario,
    }

    return render(request, "usuarios/inicio.html", context)

# Vista para cerrar sesion, que simplemente llama al logout de django y redirige a la pagina de login.
def logout_view(request):
    logout(request)
    return redirect("login")

def no_permisos(request):
    return render(request, "usuarios/no_permisos.html")