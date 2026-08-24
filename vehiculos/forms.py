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
        )

        widgets = {
            "dominio": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: AB 123 CD",
                }
            ),

            "marca": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: Toyota",
                }
            ),

            "modelo": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: Hilux",
                }
            ),

            "color": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: Blanco",
                }
            ),

            "anio": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: 2024",
                }
            ),

            "nro_chasis": forms.TextInput(
                attrs={
                    "class": "form-input form-input--mono",
                    "placeholder": "Número de chasis",
                }
            ),

            "nro_motor": forms.TextInput(
                attrs={
                    "class": "form-input form-input--mono",
                    "placeholder": "Número de motor",
                }
            ),

            "area_asignada": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Ej: Secretaría de Obras Públicas",
                }
            ),
        }