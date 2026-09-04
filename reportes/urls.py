from django.urls import path
from . import views


urlpatterns = [
    path("", views.reportes, name="reportes"),
    path("imprimir/", views.imprimir_reportes, name="imprimir_reportes"),
]