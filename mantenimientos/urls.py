from django.urls import path

from . import views


urlpatterns = [

    path(
        "vehiculo/<int:vehiculo_id>/nuevo/",
        views.nuevo_mantenimiento,
        name="nuevo_mantenimiento",
    ),

    path(
        "<int:mantenimiento_id>/",
        views.detalle_mantenimiento,
        name="detalle_mantenimiento",
    ),

    path(
        "<int:mantenimiento_id>/editar/",
        views.editar_mantenimiento,
        name="editar_mantenimiento",
    ),

    path(
        "<int:mantenimiento_id>/eliminar/",
        views.eliminar_mantenimiento,
        name="eliminar_mantenimiento",
    ),

]