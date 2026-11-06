from django.contrib import admin
from .models import TipoSolicitud, Solicitud, Perfil, Turno


# Register your models here.

@admin.register(TipoSolicitud)
class TipoSolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dias_maximos', 'requiere_respaldo', 'descuenta_saldo')

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'tipo', 'fecha_inicio', 'fecha_termino', 'estado')
    list_filter = ('tipo','estado')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dias_vacaciones')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha', 'jornada', 'hora_inicio', 'hora_termino')
    list_filter = ('jornada', 'trabajador')
    date_hierarchy = 'fecha'