from django.db import models


class Vehiculo(models.Model):

    class Estado(models.TextChoices):
        DISPONIBLE = "DISPONIBLE", "Disponible"
        EN_MANTENIMIENTO = "EN_MANTENIMIENTO", "En mantenimiento"
        FUERA_SERVICIO = "FUERA_SERVICIO", "Fuera de servicio"
        BAJA = "BAJA", "Baja"

    dominio = models.CharField(
        "Dominio (Patente)",
        max_length=10,
        unique=True,
    )

    marca = models.CharField(
        max_length=50,
    )

    modelo = models.CharField(
        max_length=50,
    )

    color = models.CharField(
        max_length=30,
    )

    nro_chasis = models.CharField(
        "N° de chasis",
        max_length=50,
    )

    nro_motor = models.CharField(
        "N° de motor",
        max_length=50,
    )

    anio = models.PositiveIntegerField(
        "Año",
        null=True,
        blank=False,
    )

    area_asignada = models.CharField(
        "Área asignada",
        max_length=100,
        blank=True,
        null=True,
    )

    estado = models.CharField(
        "Estado",
        max_length=30,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
    )

    fecha_alta = models.DateTimeField(
        "Fecha de alta en sistema",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.dominio} - {self.marca} {self.modelo}".strip()

    def reincidencias_total(self):
        return self.mantenimientos.count()