from django.shortcuts import render, redirect
from django.contrib import messages
from usuarios.serializers import UsuarioSerializer
from .models import Usuario
from tipo_usuario.models import TipoUsuario
from rest_framework import viewsets
from pistas.models import Pista
from clubs.models import Club


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        contraseña = request.POST['contraseña']
        try:
            user = Usuario.objects.get(email=email, contraseña=contraseña)
            request.session['usuario_id'] = user.id
            if user.tipo_usuario.nombre == 'manager':
                return redirect('manager_dashboard')
            if user.tipo_usuario.nombre == 'admin_club':
                return redirect('home_admin_club')
            return redirect('home')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        contraseña = request.POST['contraseña']
        tipo = request.POST['tipo_usuario']
        tipo_usuario = TipoUsuario.objects.get(nombre=tipo)
        nuevo_usuario = Usuario.objects.create(
            nombre=nombre,
            email=email,
            contraseña=contraseña,
            tipo_usuario=tipo_usuario
        )
        request.session['usuario_id'] = nuevo_usuario.id
        return redirect('home')
    tipos = TipoUsuario.objects.all()
    return render(request, 'usuarios/registro.html', {'tipos': tipos})

def home_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'usuarios/home.html', {'usuario': usuario})


def manager_dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario.tipo_usuario.nombre != 'manager':
        return redirect('home')
    return render(request, 'usuarios/manager_dashboard.html', {'user': usuario})



def home_admin_club(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    user = Usuario.objects.get(id=usuario_id)
    
    if user.tipo_usuario.nombre != 'admin_club':
        return redirect('home')

    try:
        club = Club.objects.get(usuario=user)
    except Club.DoesNotExist:
        club = None

    pistas = Pista.objects.filter(club=club) if club else []

    return render(request, 'usuarios/home_admin_club.html', {
        'user': user,
        'club': club,
        'pistas': pistas,
    })
