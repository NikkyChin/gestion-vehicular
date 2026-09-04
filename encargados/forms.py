from django import forms

from .models import Encargado, AsignacionVehiculo


class EncargadoForm(forms.ModelForm):

    class Meta:
        model = Encargado

        fields = (
            "nombre",
            "apellido",
            "dni",
            "legajo",
            "activo",
            "sector",
        )

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                "placeholder": "Ej: Juan",
            }),

            "apellido": forms.TextInput(attrs={
                "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                "placeholder": "Ej: Pérez",
            }),

            "dni": forms.TextInput(attrs={
                "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                "placeholder": "Ej: 30123456",
            }),

            "legajo": forms.TextInput(attrs={
                "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                "placeholder": "Ej: 1542",
            }),

            "activo": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500",
            }),

            "sector": forms.TextInput(attrs={
                "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                "placeholder": "Ej: Administración",
            }),
        }

    def clean_dni(self):
        dni = self.cleaned_data["dni"].strip()

        if not dni.isdigit():
            raise forms.ValidationError(
                "El DNI debe contener solamente números."
            )

        if len(dni) not in (7, 8):
            raise forms.ValidationError(
                "El DNI debe tener 7 u 8 dígitos."
            )

        return dni

    def clean_legajo(self):
        legajo = self.cleaned_data["legajo"].strip()

        if not legajo:
            raise forms.ValidationError(
                "El número de legajo es obligatorio."
            )

        return legajo

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError(
                "El nombre es obligatorio."
            )

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data["apellido"].strip()

        if not apellido:
            raise forms.ValidationError(
                "El apellido es obligatorio."
            )

        return apellido

    def clean_sector(self):
        sector = self.cleaned_data["sector"]

        if sector:
            sector = sector.strip()

        return sector


class AsignacionVehiculoForm(forms.ModelForm):

    class Meta:
        model = AsignacionVehiculo

        fields = (
            "vehiculo",
            "encargado",
            "fecha_desde",
            "fecha_hasta",
            "observaciones",
        )

        widgets = {
            "vehiculo": forms.Select(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                }
            ),

            "encargado": forms.Select(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                }
            ),

            "fecha_desde": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                }
            ),

            "fecha_hasta": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "rows": 4,
                    "placeholder": "Observaciones sobre la asignación...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Para nuevas asignaciones solamente mostramos
        # encargados que estén activos.
        self.fields["encargado"].queryset = Encargado.objects.filter(
            activo=True
        ).order_by(
            "apellido",
            "nombre",
        )