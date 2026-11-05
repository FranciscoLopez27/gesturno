from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Solicitud, TipoSolicitud
from .forms import SolicitudForm, LoginForm


# Create your views here.


def log_in(request):
    # Diccionario que almacena los datos que enviamos a la vista
    form = LoginForm(
        request.POST or None
    )
    context = {'message': None, 'form': form}
    if request.POST and form.is_valid():
        # Verificar credenciales
        # Devuelve un objeto User si las credenciales son válidas.
        # Si las credenciales no son válidas, devuelve None
        user = authenticate(**form.cleaned_data)
        if user is not None:
            # Verificar si el usuario esta activo
            if user.is_active:
                # Adjuntar usuario autenticado a la sesión actual
                login(request, user)
                # Redireccionar a una vista utilizando el nombre de la url
                return redirect('solicitudes:home')
            else:
                context['message'] = 'El usuario ha sido desactivado'
        else:
            context['message'] = 'Usuario o contraseña incorrecta'
    return render(request, 'solicitudes/login.html', context)


# decorador para restringir el acceso a solo usuarios autenticados
@login_required
def log_out(request):
    logout(request)
    return redirect('solicitudes:log-in')


@login_required
def solicitud_list(request):
    solicitudes = Solicitud.objects.filter(trabajador=request.user)
    return render(request, 'solicitudes/index.html', {'solicitudes':solicitudes})


@login_required
def solicitud_detail(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk, trabajador=request.user)

    return render(request, 'solicitudes/detail.html', {'solicitud': solicitud})


@login_required
def solicitud_create(request, **kwargs):
    form = SolicitudForm(
        request.POST or None,
        request.FILES or None
    )
    form.instance.trabajador = request.user
    if request.POST and form.is_valid():
        form.save()
        return redirect('solicitudes:home')
    return render(request, 'solicitudes/form.html', {'form': form})


@login_required
def solicitud_update(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk, trabajador=request.user, estado='pendiente')
    
    form = SolicitudForm(
        request.POST or None,
        request.FILES or None,
        instance=solicitud
    )
    if request.POST and form.is_valid():
        form.save()
        return redirect('solicitudes:home')
    return render(request, 'solicitudes/form.html', {'form': form})


@login_required
def solicitud_delete(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk, trabajador=request.user, estado='pendiente')
    if request.method == 'POST':
        solicitud.delete()
        return redirect('solicitudes:home')
    return render(request, 'solicitudes/confirm_delete.html', {'solicitud': solicitud})


@login_required
def tipo_list(request):
    tipos = TipoSolicitud.objects.all()
    return render(request, 'solicitudes/category/category_list.html', {'tipos': tipos})