from django.contrib import admin

from .models import Encargado, AsignacionVehiculo


@admin.register(Encargado)
class EncargadoAdmin(admin.ModelAdmin):

    list_display = (
        "apellido",
        "nombre",
        "dni",
        "legajo",
        "activo",
        "fecha_alta",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
        "apellido",
        "dni",
        "legajo",
    )

    ordering = (
        "apellido",
        "nombre",
    )


@admin.register(AsignacionVehiculo)
class AsignacionVehiculoAdmin(admin.ModelAdmin):

    list_display = (
        "vehiculo",
        "encargado",
        "fecha_desde",
        "fecha_hasta",
        "fecha_registro",
    )

    list_filter = (
        "fecha_desde",
        "fecha_hasta",
    )

    search_fields = (
        "vehiculo__dominio",
        "vehiculo__marca",
        "vehiculo__modelo",
        "encargado__nombre",
        "encargado__apellido",
        "encargado__dni",
        "encargado__legajo",
    )

    autocomplete_fields = (
        "vehiculo",
        "encargado",
    )

    ordering = (
        "-fecha_desde",
        "-fecha_registro",
    )