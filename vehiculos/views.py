from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from .models import Vehiculo
from .forms import EditarVehiculoForm
from encargados.models import AsignacionVehiculo


def tiene_permiso(request):
    grupos = set(request.user.groups.values_list("name", flat=True))

    return (
        "ADMINISTRATIVO" in grupos
        or "ADMIN_SISTEMA" in grupos
    )


# Nuevo vehículo en el sistema
@login_required
@transaction.atomic
def nuevo_vehiculo(request):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    if request.method == "POST":

        form = EditarVehiculoForm(request.POST)

        if form.is_valid():

            # Guardamos primero el vehículo
            vehiculo = form.save()

            # Obtenemos el encargado seleccionado
            encargado = form.cleaned_data.get("encargado")

            # Si se seleccionó un encargado, creamos la asignación
            if encargado:

                AsignacionVehiculo.objects.create(
                    vehiculo=vehiculo,
                    encargado=encargado,
                    fecha_desde=date.today(),
                )

            return redirect(
                "detalle_vehiculo",
                vehiculo_id=vehiculo.id,
            )

    else:
        form = EditarVehiculoForm()

    return render(
        request,
        "vehiculos/nuevo_vehiculo.html",
        {
            "form": form,
        },
    )


# Lista de vehículos con búsqueda
@login_required
def lista_vehiculos(request):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    q = (request.GET.get("q") or "").strip()

    vehiculos = (
        Vehiculo.objects
        .prefetch_related("asignaciones__encargado")
        .all()
        .order_by("-fecha_alta")
    )

    if q:

        vehiculos = vehiculos.filter(
            Q(dominio__icontains=q) |
            Q(marca__icontains=q) |
            Q(modelo__icontains=q) |
            Q(area_asignada__icontains=q)
        )

    return render(
        request,
        "vehiculos/lista.html",
        {
            "vehiculos": vehiculos,
            "q": q,
        },
    )


@login_required
def detalle_vehiculo(request, vehiculo_id):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    vehiculo = get_object_or_404(
        Vehiculo.objects.prefetch_related(
            "mantenimientos",
            "asignaciones__encargado",
        ),
        id=vehiculo_id,
    )

    mantenimientos = vehiculo.mantenimientos.all().order_by("-fecha")

    # Obtenemos la asignación actual
    asignacion_actual = (
        vehiculo.asignaciones
        .filter(fecha_hasta__isnull=True)
        .select_related("encargado")
        .first()
    )

    encargado_actual = (
        asignacion_actual.encargado
        if asignacion_actual
        else None
    )

    return render(
        request,
        "vehiculos/detalle_vehiculo.html",
        {
            "vehiculo": vehiculo,
            "mantenimientos": mantenimientos,
            "asignacion_actual": asignacion_actual,
            "encargado_actual": encargado_actual,
        },
    )


@login_required
def imprimir_lista_vehiculos(request):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    q = (request.GET.get("q") or "").strip()

    vehiculos = (
        Vehiculo.objects
        .prefetch_related("asignaciones__encargado")
        .all()
        .order_by("-fecha_alta")
    )

    if q:

        vehiculos = vehiculos.filter(
            Q(dominio__icontains=q) |
            Q(marca__icontains=q) |
            Q(modelo__icontains=q)
        )

    return render(
        request,
        "vehiculos/imprimir_lista.html",
        {
            "vehiculos": vehiculos,
            "q": q,
        },
    )


# Editar los datos de un vehículo
@login_required
@transaction.atomic
def editar_vehiculo(request, vehiculo_id):

    if not tiene_permiso(request):
        return render(request, "usuarios/no_permisos.html")

    vehiculo = get_object_or_404(
        Vehiculo,
        id=vehiculo_id,
    )

    # Buscamos quién está actualmente asignado
    asignacion_actual = (
        AsignacionVehiculo.objects
        .filter(
            vehiculo=vehiculo,
            fecha_hasta__isnull=True,
        )
        .select_related("encargado")
        .first()
    )

    if request.method == "POST":

        form_vehiculo = EditarVehiculoForm(
            request.POST,
            instance=vehiculo,
        )

        if form_vehiculo.is_valid():

            # Guardamos cambios propios del vehículo
            form_vehiculo.save()

            # Encargado seleccionado en el formulario
            nuevo_encargado = form_vehiculo.cleaned_data.get(
                "encargado"
            )

            encargado_actual = (
                asignacion_actual.encargado
                if asignacion_actual
                else None
            )

            # ------------------------------------------------
            # CASO 1:
            # No cambió el encargado
            # ------------------------------------------------

            if nuevo_encargado == encargado_actual:
                pass

            # ------------------------------------------------
            # CASO 2:
            # Se quitó el encargado
            # ------------------------------------------------

            elif nuevo_encargado is None:

                if asignacion_actual:

                    asignacion_actual.fecha_hasta = date.today()

                    asignacion_actual.save(
                        update_fields=["fecha_hasta"]
                    )

            # ------------------------------------------------
            # CASO 3:
            # Se asignó un nuevo encargado
            # ------------------------------------------------

            else:

                # Cerramos la asignación anterior
                if asignacion_actual:

                    # La fecha anterior termina
                    # el día anterior al nuevo encargado.
                    asignacion_actual.fecha_hasta = (
                        date.today() - timedelta(days=1)
                    )

                    asignacion_actual.save(
                        update_fields=["fecha_hasta"]
                    )

                # Creamos la nueva asignación
                AsignacionVehiculo.objects.create(
                    vehiculo=vehiculo,
                    encargado=nuevo_encargado,
                    fecha_desde=date.today(),
                )

            return redirect(
                "detalle_vehiculo",
                vehiculo_id=vehiculo.id,
            )

    else:

        form_vehiculo = EditarVehiculoForm(
            instance=vehiculo
        )

        # Mostramos el encargado actual seleccionado
        if asignacion_actual:

            form_vehiculo.fields[
                "encargado"
            ].initial = asignacion_actual.encargado

    return render(
        request,
        "vehiculos/editar_vehiculo.html",
        {
            "form_vehiculo": form_vehiculo,
            "vehiculo": vehiculo,
            "asignacion_actual": asignacion_actual,
        },
    )


def inicio(request):
    return render(
        request,
        "usuarios/inicio.html"
    )