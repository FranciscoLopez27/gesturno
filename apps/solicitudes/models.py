from datetime import timedelta
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils import timezone


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

    def dias_habiles(self):
        if not (self.fecha_inicio and self.fecha_termino):
            return 0
        dias = 0
        fecha = self.fecha_inicio
        while fecha <= self.fecha_termino:
            if fecha.weekday() < 5:
                dias += 1
            fecha += timedelta(days=1)
        return dias
    
    def estado_anterior(self):
        """Devuelve el estado guardado en la base de datos, o None si la solicitud es nueva."""
        if self.pk is None:
            return None
        return Solicitud.objects.get(pk=self.pk).estado
    
    def clean(self):
        errores = {}
        
        # Regla 1: la fecha de término no puede ser anterior a la de inicio
        if self.fecha_inicio and self.fecha_termino:
            if self.fecha_termino < self.fecha_inicio:
                errores['fecha_termino'] = 'La fecha de término no puede ser anterior a la fecha de inicio.'


        # Regla 2: al crear una solicitud, la fecha de inicio no puede estar en el pasado
        if self.pk is None and self.fecha_inicio:
            if self.fecha_inicio < timezone.localdate():
                errores['fecha_inicio'] = 'La fecha de inicio no puede ser anterior a hoy.'

        if self.tipo_id:
            # Regla 3: no superar los días máximos del tipo
            if self.tipo.dias_maximos is not None and self.dias_habiles() > self.tipo.dias_maximos:
                errores['fecha_termino'] = (
                    f'{self.tipo} permite como máximo {self.tipo.dias_maximos} días hábiles, '
                    f'y esta solicitud tiene {self.dias_habiles()}.'
                )

            # Regla 4: Si el tipo requiere respaldo, debe adjuntarse.
            if self.tipo.requiere_respaldo and not self.respaldo:
                errores['respaldo'] = f'Las solicitudes del tipo {self.tipo} requieren adjuntar un documento de respaldo.'

            # Regla 5: Se revisa si es que la solicitud no esta aprobada, y que tenga la cantidad de dias disponibles necesarios en caso de descontar (vacaciones).
            if self.tipo.descuenta_saldo and self.estado_anterior() != 'aprobada' and self.trabajador_id:
                perfil = Perfil.objects.filter(usuario_id=self.trabajador_id).first()
                saldo = perfil.dias_vacaciones if perfil else 0
                if self.dias_habiles() > saldo:
                    errores['fecha_termino'] = (f'La solicitud tiene {self.dias_habiles()} días hábiles, pero el saldo de vacaciones disponible es de {saldo} días')

        if errores:
            raise ValidationError(errores)

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