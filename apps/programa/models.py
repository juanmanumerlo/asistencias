from datetime import date, datetime
from django.db import models

from apps.core.models import ModeloBase
from apps.persona.models import Persona


class TipoAsistencia(ModeloBase):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150,
                                   unique=True)

    def __str__(self):
        return self.descripcion


class Programa(ModeloBase):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    tipo_asistencias = models.ManyToManyField(TipoAsistencia)
    requisitos = models.FileField(upload_to="requisitos", blank=True)
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class AsignacionBeneficio(ModeloBase):
    id = models.AutoField(primary_key=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipo_asistencia = models.ForeignKey(TipoAsistencia, on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField(default=datetime.today)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "{} recibió el beneficio: {}".format(self.persona, self.tipo_asistencia)
