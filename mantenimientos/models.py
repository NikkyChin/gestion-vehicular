from django.db import models


class Mantenimiento(models.Model):

    class Tipo(models.TextChoices):
        SERVICE = "SERVICE", "Service"
        REPARACION = "REPARACION", "Reparación"
        CAMBIO_ACEITE = "CAMBIO_ACEITE", "Cambio de aceite"
        REVISION = "REVISION", "Revisión"
        NEUMATICOS = "NEUMATICOS", "Neumáticos"
        ELECTRICO = "ELECTRICO", "Sistema eléctrico"
        CHAPA_PINTURA = "CHAPA_PINTURA", "Chapa y pintura"
        OTRO = "OTRO", "Otro"

    vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="Vehículo",
    )

    tipo = models.CharField(
        "Tipo de mantenimiento",
        max_length=30,
        choices=Tipo.choices,
    )

    descripcion = models.TextField(
        "Descripción",
    )

    fecha = models.DateField(
        "Fecha de mantenimiento",
    )

    fecha_ingreso = models.DateField(
        "Fecha de ingreso al taller",
        null=True,
        blank=True,
    )

    fecha_salida = models.DateField(
        "Fecha de salida del taller",
        null=True,
        blank=True,
    )

    proveedor = models.CharField(
        "Proveedor / Taller",
        max_length=150,
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

    fecha_modificacion = models.DateTimeField(
        "Última modificación",
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.vehiculo.dominio} - "
            f"{self.get_tipo_display()} - "
            f"{self.fecha}"
        )

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha", "-fecha_registro"]