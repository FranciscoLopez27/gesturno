from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


# Create your models here.

class BaseModel(models.Model):
    creado = models.DateTimeField(auto_now=False, auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True



class TipoSolicitud(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)
    dias_maximos = models.PositiveIntegerField('días máximos por solicitud', null=True, blank=True,
                                            help_text='Dejar vacío si no hay un máximo fijo.')
    requiere_respaldo = models.BooleanField('requiere un documento de respaldo',default=False)
    descuenta_saldo = models.BooleanField('descuenta del saldo de vacaciones',default=False)

    class Meta:
        verbose_name = 'Tipo de solicitud'
        verbose_name_plural = 'Tipos de solicitudes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Solicitud(BaseModel):
    ESTADOS = [('pendiente','Pendiente'),('aprobada','Aprobada'),('rechazada','Rechazada')]
    
    
    trabajador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='solicitudes', verbose_name='trabajador'
    )
    tipo = models.ForeignKey(
        TipoSolicitud, on_delete=models.PROTECT, verbose_name='tipo de solicitud'
    )
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_termino = models.DateField('fecha de término')
    motivo = models.TextField('motivo o comentario', max_length=500, blank=True)
    respaldo = models.FileField('documento de respaldo', upload_to='respaldos/', null=True, blank=True)
    estado = models.CharField('estado', max_length=20, choices=ESTADOS, default='pendiente')
    
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ["-creado"]

    def __str__(self):
        return f'{self.tipo} - {self.trabajador} ({self.fecha_inicio} al {self.fecha_termino})'
    
    def get_edit_url(self):
        return reverse_lazy('solicitudes:solicitud-editar', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('solicitudes:solicitud-eliminar', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('solicitudes:solicitud-detalle', kwargs={'pk': self.pk})


class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='perfil', verbose_name='usuario'
    )

    dias_vacaciones = models.PositiveIntegerField('días de vacaciones disponibles',default=0)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.usuario}'