from django.db import models

# Create your models here.
from django.db import models


class Encargado(models.Model):

    nombre = models.CharField(
        "Nombre",
        max_length=100,
    )

    apellido = models.CharField(
        "Apellido",
        max_length=100,
    )

    dni = models.CharField(
        "DNI",
        max_length=20,
        unique=True,
    )

    legajo = models.CharField(
        "N° de legajo",
        max_length=20,
        unique=True,
    )

    sector = models.CharField(
        "Sector",
        max_length=100,
        blank=True,
        null=True,
    )

    activo = models.BooleanField(
        "Activo",
        default=True,
    )

    fecha_alta = models.DateTimeField(
        "Fecha de alta en sistema",
        auto_now_add=True,
    )

    fecha_modificacion = models.DateTimeField(
        "Última modificación",
        auto_now=True,
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "Encargado"
        verbose_name_plural = "Encargados"
        ordering = ["apellido", "nombre"]


class AsignacionVehiculo(models.Model):

    vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        on_delete=models.PROTECT,
        related_name="asignaciones",
        verbose_name="Vehículo",
    )

    encargado = models.ForeignKey(
        Encargado,
        on_delete=models.PROTECT,
        related_name="asignaciones",
        verbose_name="Encargado",
    )

    fecha_desde = models.DateField(
        "Fecha desde",
    )

    fecha_hasta = models.DateField(
        "Fecha hasta",
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        "Observaciones",
        blank=True,
    )

    fecha_registro = models.DateTimeField(
        "Fecha de registro",
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.encargado} - "
            f"{self.vehiculo.dominio} - "
            f"{self.fecha_desde}"
        )

    class Meta:
        verbose_name = "Asignación de vehículo"
        verbose_name_plural = "Asignaciones de vehículos"
        ordering = ["-fecha_desde", "-fecha_registro"]

        constraints = [
            models.UniqueConstraint(
                fields=["vehiculo"],
                condition=models.Q(fecha_hasta__isnull=True),
                name="una_asignacion_activa_por_vehiculo",
            ),
        ]

