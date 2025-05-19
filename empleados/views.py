from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .models import Horario, Mensaje


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel')
    else:
        form = AuthenticationForm()
    return render(request, 'empleados/login.html', {'form': form})

@login_required
def panel_empleado(request):
    usuario = request.user
    horarios = Horario.objects.filter(empleado=usuario)
    mensajes = Mensaje.objects.filter(destinatario=usuario).order_by('-fecha')
    return render(request, 'empleados/panel.html', {
        'usuario': usuario,
        'horarios': horarios,
        'mensajes': mensajes,
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


from .forms import RegistroUsuarioForm

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'empleados/registro.html', {'form': form})
