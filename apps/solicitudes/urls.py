from django.urls import re_path, include
from apps.solicitudes import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'solicitudes'

solicitudes_patterns = [
    re_path(r'^inicio/$', views.solicitud_list, name='home'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.solicitud_detail, name='solicitud-detalle'),
    re_path(r'^crear/$', views.solicitud_create, name='solicitud-crear'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.solicitud_update, name='solicitud-editar'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.solicitud_delete, name='solicitud-eliminar')
]

urlpatterns = [
    re_path(r'^$', views.log_in, name='log-in'),
    re_path(r'^log-out/$', views.log_out, name='log-out'),
    re_path(r'^tipos/$', views.tipo_list, name='tipos-lista'),
    re_path(r'^solicitudes/', include(solicitudes_patterns)),
    re_path(r'^turnos/$', views.turno_list, name='mis-turnos')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)