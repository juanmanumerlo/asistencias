from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput

from .models import Programa, AsignacionBeneficio


class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ('nombre', 'tipo_asistencias', 'requisitos', 'fecha_inicio', 'fecha_fin')

        widgets = {
            'requisitos': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin': DateInput(format='%y-%m-%d', attrs={'type': 'date'})
        }

    def clean_requisitos(self):
        requisitos = self.cleaned_data['requisitos']
        if requisitos:
            extension = requisitos.name.rsplit('.', 1)[1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
        return requisitos

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = self.cleaned_data['fecha_inicio']
        fecha_fin = self.cleaned_data['fecha_fin']
        # Verifica que la fecha de inicio sea anterior a fecha fin.
        if fecha_fin and fecha_inicio > fecha_fin:
            raise ValidationError(
                {'fecha_inicio': 'La Fecha de Inicio no puede ser posterior que la fecha fin'},
                code='invalido'
            )
        return cleaned_data


class AsignacionForm(forms.ModelForm):
    class Meta:
        model = AsignacionBeneficio
        fields = ('programa', 'persona', 'tipo_asistencia', 'fecha_entrega', 'cantidad')

        widgets = {
            'fecha_entrega': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

        def clean_fecha(self):
            fecha_entrega = self.cleaned_data['fecha_entrega']
            fecha_ahora = date.today
            # Verifica que la fecha de asignacion no sea posterior a la fecha de hoy.
            if fecha_entrega and fecha_entrega < fecha_ahora:
                raise ValidationError(
                    {'fecha_entrega': 'La Fecha de Asigancion de un Beneficio no puede ser posterior a la fecha de hoy'},
                    code='invalido'
                )
            return fecha_entrega

        def clean_cantidad(self):
            cantidad = self.cleaned_data['cantidad']
            # Verifica que la cantidad de beneficios no sea menor a 1.
            if cantidad < 1.00:
                raise ValidationError(
                    {'cantidad': 'La cantidad de beneficios por asignacion no puede ser menor a 1'},
                    code='invalido'
                )
            return cantidad
