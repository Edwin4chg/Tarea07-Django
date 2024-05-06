from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .forms import EventoForm
from .forms import RegistroEventoForm
from .models import Evento, RegistroEvento, Usuario
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    user = request.user  
    return render(request, 'home.html', {'user': user})


def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventoForm()
    return render(request, 'evento.html', {'form': form})

def registro_evento(request):
    eventos = Evento.objects.all()
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        usuario_id = request.POST.get('usuario_id')
        evento = get_object_or_404(Evento, id=evento_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)
        RegistroEvento.objects.create(usuario=usuario, evento=evento)
        return redirect('registro_evento')  # Redirige a la misma página para actualizar la lista de eventos
    else:
        form = RegistroEventoForm()
    return render(request, 'registro_evento.html', {'eventos': eventos, 'form': form})


def detalles_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'detalles_evento.html', {'eventos': eventos})

@login_required
def mis_registros_eventos(request):
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        usuario_id = request.user.id
        
        if 'desuscribir' in request.POST:
            RegistroEvento.objects.filter(usuario_id=usuario_id, evento_id=evento_id).delete()
        else:
            RegistroEvento.objects.create(usuario_id=usuario_id, evento_id=evento_id)

        return redirect('mis_registros_eventos')
    else:
        registros_eventos = RegistroEvento.objects.filter(usuario_id=request.user.id)
        return render(request, 'mis_registros_eventos.html', {'registros_eventos': registros_eventos})


def cerrar_sesion(request):
    logout(request)
    return redirect('login') 