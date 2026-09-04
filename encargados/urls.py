from django.urls import path

from . import views


urlpatterns = [
    path("", views.lista_encargados, name="lista_encargados"),
    path("nuevo/", views.nuevo_encargado, name="nuevo_encargado"),
    path("<int:encargado_id>/", views.detalle_encargado, name="detalle_encargado"),
    path("<int:encargado_id>/editar/", views.editar_encargado, name="editar_encargado"),
    path("<int:encargado_id>/dar-de-baja/", views.dar_de_baja_encargado, name="dar_de_baja_encargado"),
]