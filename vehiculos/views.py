from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,  get_object_or_404
from .models import Vehiculo
from .forms import EditarVehiculoForm
from django.db.models import Q

# Nuevo vehículo en el sistema
@login_required
def nuevo_vehiculo(request):
    grupos = set(request.user.groups.values_list("name", flat=True))
    if "ADMINISTRATIVO" not in grupos and "ADMIN_SISTEMA" not in grupos:
        return render(request, "usuarios/no_permisos.html")

    if request.method == "POST":
        form = EditarVehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            return redirect("detalle_vehiculo", vehiculo_id=vehiculo.id)
    else:
        form = EditarVehiculoForm()

    return render(request, "vehiculos/nuevo_vehiculo.html", {"form": form})

# Lista de vehículos con búsqueda
@login_required
def lista_vehiculos(request):
    grupos = set(request.user.groups.values_list("name", flat=True))

    if "ADMINISTRATIVO" not in grupos and "ADMIN_SISTEMA" not in grupos:
        return render(request, "usuarios/no_permisos.html")

    q = (request.GET.get("q") or "").strip()

    vehiculos = Vehiculo.objects.all().order_by("-fecha_alta")
    if q:
        vehiculos = vehiculos.filter(
            Q(dominio__icontains=q) |
            Q(marca__icontains=q) |
            Q(modelo__icontains=q) |
            Q(area_asignada__icontains=q)
        )

    return render(request, "vehiculos/lista.html", {"vehiculos": vehiculos, "q": q})

@login_required
def detalle_vehiculo(request, vehiculo_id):
    grupos = set(request.user.groups.values_list("name", flat=True))
    if "ADMINISTRATIVO" not in grupos and "ADMIN_SISTEMA" not in grupos:
        return render(request, "usuarios/no_permisos.html")

    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    return render(
        request,
        "vehiculos/detalle_vehiculo.html",
        {"vehiculo": vehiculo},
    )


@login_required
def imprimir_lista_vehiculos(request):
    q = (request.GET.get("q") or "").strip()

    vehiculos = Vehiculo.objects.all().order_by("-fecha_alta")

    if q:
        vehiculos = vehiculos.filter(
            Q(dominio__icontains=q) |
            Q(marca__icontains=q) |
            Q(modelo__icontains=q)
        )

    return render(request, "vehiculos/imprimir_lista.html", {"vehiculos": vehiculos, "q": q})

# Vista para editar los datos de un vehículo registrado en el sistema, como dominio, marca, modelo, color, año, número de chasis y número de motor.
@login_required
def editar_vehiculo(request, vehiculo_id):
    grupos = set(request.user.groups.values_list("name", flat=True))
    if "ADMINISTRATIVO" not in grupos and "ADMIN_SISTEMA" not in grupos:
        return render(request, "usuarios/no_permisos.html")

    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "POST":
        form_vehiculo = EditarVehiculoForm(request.POST, instance=vehiculo)
        if form_vehiculo.is_valid():
            form_vehiculo.save()
            return redirect("detalle_vehiculo", vehiculo_id=vehiculo.id)
    else:
        form_vehiculo = EditarVehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/editar_vehiculo.html", {"form_vehiculo": form_vehiculo, "vehiculo": vehiculo})


def inicio(request):
    return render(request, "usuarios/inicio.html")