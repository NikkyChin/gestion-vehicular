from django.contrib import admin
from .models import Vehiculo

# Registro de los modelos de vehículos, ingresos al sistema y lugares del sistema en el admin de Django, para poder ver y editar estos datos desde el panel de administración.
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):

    list_display = (
        "dominio",
        "marca",
        "modelo",
        "color",
        "anio",
        "estado",
        "fecha_alta",
        "area_asignada",
    )

    list_filter = (
        "estado",
        "marca",
        "color",
        "anio",
    )

    search_fields = (
        "dominio",
        "marca",
        "modelo",
        "nro_chasis",
        "nro_motor",
        "area_asignada",
    )