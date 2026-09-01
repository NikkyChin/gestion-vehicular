from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .models import Mantenimiento
from .forms import MantenimientoForm

from vehiculos.models import Vehiculo


def tiene_permiso(request):
    grupos = set(request.user.groups.values_list("name", flat=True))
    return "ADMINISTRATIVO" in grupos or "ADMIN_SISTEMA" in grupos


@login_required
def nuevo_mantenimiento(request, vehiculo_id):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "POST":

        form = MantenimientoForm(request.POST)

        if form.is_valid():

            mantenimiento = form.save(commit=False)

            mantenimiento.vehiculo = vehiculo

            mantenimiento.save()

            return redirect(
                "detalle_vehiculo",
                vehiculo_id=vehiculo.id,
            )

    else:
        form = MantenimientoForm()

    return render(
        request,
        "mantenimientos/nuevo_mantenimiento.html",
        {
            "form": form,
            "vehiculo": vehiculo,
        },
    )


@login_required
def detalle_mantenimiento(request, mantenimiento_id):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    mantenimiento = get_object_or_404(
        Mantenimiento.objects.select_related("vehiculo"),
        id=mantenimiento_id,
    )

    return render(
        request,
        "mantenimientos/detalle_mantenimiento.html",
        {
            "mantenimiento": mantenimiento,
        },
    )


@login_required
def editar_mantenimiento(request, mantenimiento_id):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    mantenimiento = get_object_or_404(
        Mantenimiento.objects.select_related("vehiculo"),
        id=mantenimiento_id,
    )

    if request.method == "POST":

        form = MantenimientoForm(
            request.POST,
            instance=mantenimiento,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "detalle_vehiculo",
                vehiculo_id=mantenimiento.vehiculo.id,
            )

    else:

        form = MantenimientoForm(
            instance=mantenimiento,
        )

    return render(
        request,
        "mantenimientos/editar_mantenimiento.html",
        {
            "form": form,
            "mantenimiento": mantenimiento,
            "vehiculo": mantenimiento.vehiculo,
        },
    )


@login_required
def eliminar_mantenimiento(request, mantenimiento_id):
    grupos = set(request.user.groups.values_list("name", flat=True))

    if "ADMIN_SISTEMA" not in grupos:
            return render(request, "usuarios/no_permisos.html")

    mantenimiento = get_object_or_404(
        Mantenimiento.objects.select_related("vehiculo"),
        id=mantenimiento_id,
    )

    vehiculo_id = mantenimiento.vehiculo.id

    if request.method == "POST":
        mantenimiento.delete()

        return redirect(
            "detalle_vehiculo",
            vehiculo_id=vehiculo_id,
        )

    return render(
        request,
        "mantenimientos/eliminar_mantenimiento.html",
        {
            "mantenimiento": mantenimiento,
        },
    )