
from django.urls import re_path, include
from apps.solicitudes import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'solicitudes'

movies_patterns = [
    re_path(r'^inicio/$', views.movie_list, name='home'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.movie_detail, name='movies-detail'),
    re_path(r'^crear/$', views.movie_create, name='movies-create'),
    re_path(r'^(?P<pk>[0-9]+)/editar/$', views.movie_update, name='movies-edit'),
    re_path(r'^(?P<pk>[0-9]+)/eliminar/$', views.movie_delete, name='movies-delete')
]

urlpatterns = [
    re_path(r'^$', views.log_in, name='log-in'),
    re_path(r'^log-out/$', views.log_out, name='log-out'),
    re_path(r'^categorias/$', views.category_list, name='category-list'),
    re_path(r'^peliculas/', include(movies_patterns))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)