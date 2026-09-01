from django.contrib import admin
from .models import Mantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):

    list_display = (
        "vehiculo",
        "tipo",
        "fecha",
        "fecha_ingreso",
        "fecha_salida",
        "proveedor",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "vehiculo__dominio",
        "vehiculo__marca",
        "vehiculo__modelo",
        "proveedor",
        "descripcion",
    )

    autocomplete_fields = (
        "vehiculo",
    )

    ordering = (
        "-fecha",
        "-fecha_registro",
    )