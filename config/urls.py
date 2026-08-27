from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('usuarios.urls')),
    path('admin/', admin.site.urls),
    path("vehiculos/", include("vehiculos.urls")),  
    path("usuarios/", include("usuarios.urls")),
]
