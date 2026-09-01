from django import forms
from .models import Mantenimiento


class MantenimientoForm(forms.ModelForm):

    class Meta:
        model = Mantenimiento

        fields = (
            "tipo",
            "descripcion",
            "fecha",
            "fecha_ingreso",
            "fecha_salida",
            "proveedor",
            "observaciones",
        )

        widgets = {
            "tipo": forms.Select(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "placeholder": "Describa el mantenimiento realizado...",
                    "rows": 4,
                }
            ),

            "fecha": forms.DateInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "type": "date",
                }
            ),

            "fecha_ingreso": forms.DateInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "type": "date",
                }
            ),

            "fecha_salida": forms.DateInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "type": "date",
                }
            ),

            "proveedor": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "placeholder": "Ej: Taller Municipal",
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-2 rounded-md w-full",
                    "placeholder": "Observaciones adicionales...",
                    "rows": 3,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        fecha_ingreso = cleaned_data.get("fecha_ingreso")
        fecha_salida = cleaned_data.get("fecha_salida")

        if fecha_ingreso and fecha_salida:
            if fecha_salida < fecha_ingreso:
                raise forms.ValidationError(
                    "La fecha de salida no puede ser anterior a la fecha de ingreso."
                )

        return cleaned_data