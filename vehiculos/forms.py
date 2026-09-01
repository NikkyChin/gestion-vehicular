from django import forms
from .models import Vehiculo


class EditarVehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo

        fields = (
            "dominio",
            "marca",
            "modelo",
            "color",
            "anio",
            "nro_chasis",
            "nro_motor",
            "area_asignada",
            "estado",
        )

        widgets = {
            "dominio": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: AB 123 CD",
                }
            ),

            "marca": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: Toyota",
                }
            ),

            "modelo": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: Hilux",
                }
            ),

            "color": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: Blanco",
                }
            ),

            "anio": forms.NumberInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: 2024",
                }
            ),

            "nro_chasis": forms.TextInput(
                attrs={
                    "class": "form-input form-input--mono border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Número de chasis",
                }
            ),

            "nro_motor": forms.TextInput(
                attrs={
                    "class": "form-input form-input--mono border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Número de motor",
                }
            ),

            "area_asignada": forms.TextInput(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md",
                    "placeholder": "Ej: Secretaría de Obras Públicas",
                }
            ),
            
            "estado": forms.Select(
                attrs={
                    "class": "form-input border border-black bg-slate-50 px-2 py-1 rounded-md w-full",
                }
            ),
        }