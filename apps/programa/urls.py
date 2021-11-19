from django.urls import path
from .views import programa_lista, programa_detalle, programa_create, programa_edit, programa_delete, asignacion_create, \
    asignacion_lista

app_name = 'programa'
urlpatterns = [
    # programa views
    path('', programa_lista, name='programa_lista'),
    path('<int:pk>/', programa_detalle, name='programa_detalle'),
    path('create/', programa_create, name='programa_create'),
    path('edit/<int:pk>', programa_edit, name='programa_edit'),
    path('delete/', programa_delete, name='programa_delete'),
    path('asignacion/crear/', asignacion_create, name='asignacion'),
    path('asignacion/<int:pk>/', asignacion_lista, name='asignacion_lista'),
]
