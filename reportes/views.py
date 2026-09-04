from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from vehiculos.models import Vehiculo
from encargados.models import Encargado, AsignacionVehiculo
from mantenimientos.models import Mantenimiento


def tiene_permiso(request):
    grupos = set(request.user.groups.values_list("name", flat=True))
    return "ADMINISTRATIVO" in grupos or "ADMIN_SISTEMA" in grupos


@login_required
def reportes(request):
    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    # -------------------------
    # VEHÍCULOS
    # -------------------------

    total_vehiculos = Vehiculo.objects.count()

    vehiculos_por_estado = (
        Vehiculo.objects
        .values("estado")
        .annotate(total=Count("id"))
        .order_by("estado")
    )

    # -------------------------
    # ENCARGADOS
    # -------------------------

    total_encargados = Encargado.objects.count()

    encargados_activos = Encargado.objects.filter(
        activo=True
    ).count()

    vehiculos_con_encargado = (
        AsignacionVehiculo.objects
        .filter(fecha_hasta__isnull=True)
        .count()
    )

    vehiculos_sin_encargado = (
        total_vehiculos - vehiculos_con_encargado
    )

    # -------------------------
    # MANTENIMIENTOS
    # -------------------------

    total_mantenimientos = Mantenimiento.objects.count()

    mantenimientos_por_tipo = (
        Mantenimiento.objects
        .values("tipo")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(
        request,
        "reportes/reportes.html",
        {
            "total_vehiculos": total_vehiculos,
            "vehiculos_por_estado": vehiculos_por_estado,

            "total_encargados": total_encargados,
            "encargados_activos": encargados_activos,
            "vehiculos_con_encargado": vehiculos_con_encargado,
            "vehiculos_sin_encargado": vehiculos_sin_encargado,

            "total_mantenimientos": total_mantenimientos,
            "mantenimientos_por_tipo": mantenimientos_por_tipo,
        },
    )

@login_required
def imprimir_reportes(request):
    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    total_vehiculos = Vehiculo.objects.count()

    vehiculos_por_estado = (
        Vehiculo.objects
        .values("estado")
        .annotate(total=Count("id"))
        .order_by("estado")
    )

    total_encargados = Encargado.objects.count()

    encargados_activos = Encargado.objects.filter(
        activo=True
    ).count()

    vehiculos_con_encargado = (
        AsignacionVehiculo.objects
        .filter(fecha_hasta__isnull=True)
        .count()
    )

    vehiculos_sin_encargado = (
        total_vehiculos - vehiculos_con_encargado
    )

    total_mantenimientos = Mantenimiento.objects.count()

    mantenimientos_por_tipo = (
        Mantenimiento.objects
        .values("tipo")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(
        request,
        "reportes/imprimir_reportes.html",
        {
            "total_vehiculos": total_vehiculos,
            "vehiculos_por_estado": vehiculos_por_estado,
            "total_encargados": total_encargados,
            "encargados_activos": encargados_activos,
            "vehiculos_con_encargado": vehiculos_con_encargado,
            "vehiculos_sin_encargado": vehiculos_sin_encargado,
            "total_mantenimientos": total_mantenimientos,
            "mantenimientos_por_tipo": mantenimientos_por_tipo,
        },
    )