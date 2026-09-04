from datetime import date

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EncargadoForm
from .models import Encargado, AsignacionVehiculo


def tiene_permiso(request):
    grupos = set(request.user.groups.values_list("name", flat=True))

    return (
        "ADMINISTRATIVO" in grupos
        or "ADMIN_SISTEMA" in grupos
    )


@login_required
def lista_encargados(request):

    if not tiene_permiso(request):
        return render(
            request,
            "usuarios/no_permisos.html"
        )

    q = (request.GET.get("q") or "").strip()

    encargados = Encargado.objects.all().order_by(
        "apellido",
        "nombre",
    )

    if q:
        encargados = encargados.filter(
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(dni__icontains=q) |
            Q(legajo__icontains=q)
        )

    return render(
        request,
        "encargados/lista_encargados.html",
        {
            "encargados": encargados,
            "q": q,
        },
    )


@login_required
def nuevo_encargado(request):

    if not tiene_permiso(request):
        return render(
            request,
            "usuarios/no_permisos.html"
        )

    if request.method == "POST":

        form = EncargadoForm(request.POST)

        if form.is_valid():

            encargado = form.save()

            return redirect(
                "detalle_encargado",
                encargado_id=encargado.id,
            )

    else:
        form = EncargadoForm()

    return render(
        request,
        "encargados/nuevo_encargado.html",
        {
            "form": form,
        },
    )


@login_required
def detalle_encargado(request, encargado_id):

    if not tiene_permiso(request):
        return render(
            request,
            "usuarios/no_permisos.html"
        )

    encargado = get_object_or_404(
        Encargado,
        id=encargado_id,
    )

    asignaciones = (
        AsignacionVehiculo.objects
        .filter(encargado=encargado)
        .select_related("vehiculo")
        .order_by("-fecha_desde")
    )

    asignaciones_actuales = asignaciones.filter(
        fecha_hasta__isnull=True
    )

    asignaciones_historicas = asignaciones.filter(
        fecha_hasta__isnull=False
    )

    return render(
        request,
        "encargados/detalle_encargado.html",
        {
            "encargado": encargado,
            "asignaciones_actuales": asignaciones_actuales,
            "asignaciones_historicas": asignaciones_historicas,
        },
    )


@login_required
def editar_encargado(request, encargado_id):

    if not tiene_permiso(request):
        return render(
            request,
            "usuarios/no_permisos.html"
        )

    encargado = get_object_or_404(
        Encargado,
        id=encargado_id,
    )

    if request.method == "POST":

        form = EncargadoForm(
            request.POST,
            instance=encargado,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "detalle_encargado",
                encargado_id=encargado.id,
            )

    else:

        form = EncargadoForm(
            instance=encargado
        )

    return render(
        request,
        "encargados/editar_encargado.html",
        {
            "form": form,
            "encargado": encargado,
        },
    )


@login_required
@transaction.atomic
def dar_de_baja_encargado(request, encargado_id):

    if not tiene_permiso(request):
        return render(
            request,
            "usuarios/no_permisos.html"
        )

    encargado = get_object_or_404(
        Encargado,
        id=encargado_id,
    )

    if request.method == "POST":

        # Si ya está dado de baja, no hacemos nada.
        if encargado.activo:

            encargado.activo = False
            encargado.save(update_fields=["activo"])

            # Cerramos todas las asignaciones actuales.
            AsignacionVehiculo.objects.filter(
                encargado=encargado,
                fecha_hasta__isnull=True,
            ).update(
                fecha_hasta=date.today()
            )

        return redirect(
            "detalle_encargado",
            encargado_id=encargado.id,
        )

    return render(
        request,
        "encargados/dar_de_baja.html",
        {
            "encargado": encargado,
        },
    )