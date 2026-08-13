from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("nuevo/", views.nuevo_vehiculo, name="nuevo_vehiculo"),
    path("lista/", views.lista_vehiculos, name="lista_vehiculos"),
    path("vehiculo/<int:vehiculo_id>/", views.detalle_vehiculo, name="detalle_vehiculo"),
    path("imprimir/", views.imprimir_lista_vehiculos, name="imprimir_lista_vehiculos"),
    path("vehiculo/<int:vehiculo_id>/editar/", views.editar_vehiculo, name="editar_vehiculo"),
    
]
