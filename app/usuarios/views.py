from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.usuarios.serializers import UsuarioSerializer
from .models import Usuario
from app.tipo_usuario.models import TipoUsuario
from rest_framework import viewsets
from app.pistas.models import Pista
from app.clubs.models import Club
from app.decorators import login_required_custom, manager_required, admin_club_required, jugador_required


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


def login_view(request):
    # Si ya está logueado, redirigir según su tipo
    if request.session.get('usuario_id'):
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            user_type = usuario.tipo_usuario.nombre if usuario.tipo_usuario else None
            if user_type == 'manager':
                return redirect('manager_dashboard')
            elif user_type == 'admin_club':
                return redirect('home_admin_club')
            elif user_type == 'jugador':
                return redirect('home')
        except Usuario.DoesNotExist:
            request.session.flush()
    
    if request.method == 'POST':
        email = request.POST['email']
        contraseña = request.POST['contraseña']
        try:
            user = Usuario.objects.get(email=email, contraseña=contraseña)
            request.session['usuario_id'] = user.id
            
            # Redirigir según el tipo de usuario
            user_type = user.tipo_usuario.nombre if user.tipo_usuario else None
            if user_type == 'manager':
                return redirect('manager_dashboard')
            elif user_type == 'admin_club':
                return redirect('home_admin_club')
            else:
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


@jugador_required
def home_view(request):
    # Ya tienes el usuario en request.current_user gracias al decorador
    return render(request, 'usuarios/home.html', {'usuario': request.current_user})


@manager_required
def manager_dashboard(request):
    # Ya tienes el usuario en request.current_user gracias al decorador
    context = {
        'user': request.current_user,
        'total_usuarios': Usuario.objects.count(),
        'total_clubs': Club.objects.count(),
        'total_pistas': Pista.objects.count(),
    }
    return render(request, 'usuarios/manager_dashboard.html', context)


@admin_club_required
def home_admin_club(request):
    # Ya tienes el usuario en request.current_user gracias al decorador
    user = request.current_user
    
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


# Vistas CRUD de usuarios - Solo para managers
@manager_required
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuario_list.html', {'usuarios': usuarios})


@manager_required
def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/usuario_detail.html', {'usuario': usuario})


@manager_required
def usuario_create(request):
    tipos = TipoUsuario.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        nivel_padel = request.POST.get('nivel_padel') or None
        foto_perfil_url = request.POST.get('foto_perfil_url')
        tipo_usuario_id = request.POST.get('tipo_usuario')
        tipo_usuario = get_object_or_404(TipoUsuario, pk=tipo_usuario_id)

        Usuario.objects.create(
            nombre=nombre,
            email=email,
            contraseña=contraseña,
            nivel_padel=nivel_padel,
            foto_perfil_url=foto_perfil_url,
            tipo_usuario=tipo_usuario,
        )
        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuario-list')

    return render(request, 'usuarios/usuario_form.html', {'tipos': tipos})


@manager_required
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    tipos = TipoUsuario.objects.all()
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.email = request.POST.get('email')
        usuario.contraseña = request.POST.get('contraseña')
        usuario.nivel_padel = request.POST.get('nivel_padel') or None
        usuario.foto_perfil_url = request.POST.get('foto_perfil_url')
        tipo_usuario_id = request.POST.get('tipo_usuario')
        usuario.tipo_usuario = get_object_or_404(TipoUsuario, pk=tipo_usuario_id)
        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente')
        return redirect('usuario-list')

    return render(request, 'usuarios/usuario_form.html', {'usuario': usuario, 'tipos': tipos})


@manager_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente')
        return redirect('usuario-list')
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})
