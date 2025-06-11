from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.usuarios.serializers import UsuarioSerializer
from .models import Usuario
from app.tipo_usuario.models import TipoUsuario
from rest_framework import viewsets
from app.pistas.models import Pista
from app.clubs.models import Club
from app.decorators import login_required_custom, manager_required, admin_club_required, jugador_required
from app.invitaciones.models import Invitaciones
from app.partidos.models import Partido
from app.usuarios.models import Usuario
from app.clubs.models import Club
from app.pistas.models import Pista
from app.estado_reserva.models import EstadoReserva
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import date, datetime
from django.http import JsonResponse
import json
from django.views.decorators.http import require_GET

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
                return redirect('home_jugador')
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
                return redirect('home_jugador')
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



@login_required_custom
@jugador_required
def home_jugador(request):
    """
    Vista principal para jugadores - Dashboard con invitaciones y partidos
    """
    usuario = request.current_user
    
    # Invitaciones pendientes (donde el usuario fue invitado)
    invitaciones_pendientes = Invitaciones.objects.filter(
        invitado_email=usuario.email,
        estado='pendiente'
    ).select_related('usuario', 'partido__club', 'partido__pista').order_by('-id')
    
    # Invitaciones aceptadas (donde el usuario fue invitado)
    invitaciones_aceptadas = Invitaciones.objects.filter(
        invitado_email=usuario.email,
        estado='aceptada'
    ).select_related('usuario', 'partido__club', 'partido__pista').order_by('-id')
    
    # Partidos próximos (partidos del usuario + partidos de invitaciones aceptadas)
    hoy = date.today()
    
    # Partidos creados por el usuario
    partidos_usuario = Partido.objects.filter(
        usuario=usuario,
        fecha__gte=hoy
    )
    
    # Partidos donde fue invitado y aceptó
    partidos_invitado_ids = invitaciones_aceptadas.values_list('partido_id', flat=True)
    partidos_invitado = Partido.objects.filter(
        id__in=partidos_invitado_ids,
        fecha__gte=hoy
    )
    
    # Combinar ambos querysets
    partidos_proximos = (partidos_usuario | partidos_invitado).distinct().select_related(
        'club', 'pista', 'estado_reserva'
    ).order_by('fecha', 'hora_inicio')[:10]
    
    context = {
        'usuario': usuario,
        'invitaciones_pendientes': invitaciones_pendientes,
        'invitaciones_aceptadas': invitaciones_aceptadas,
        'partidos_proximos': partidos_proximos,
    }
    
    return render(request, 'usuarios/home_jugador.html', context)


@login_required_custom
@jugador_required
def aceptar_invitacion(request, invitacion_id):
    """
    Acepta una invitación pendiente y crea un nuevo partido para el usuario invitado
    """
    if request.method == 'POST':
        invitacion = get_object_or_404(
            Invitaciones,
            id=invitacion_id,
            invitado_email=request.current_user.email,
            estado='pendiente'
        )
        
        # Cambiar estado de la invitación
        invitacion.estado = 'aceptada'
        invitacion.save()
        
        # Crear un nuevo partido para el usuario que aceptó la invitación
        # Basado en los datos del partido original
        partido_original = invitacion.partido
        
        try:
            # Crear nuevo partido con los mismos datos pero diferente usuario
            nuevo_partido = Partido.objects.create(
                fecha=partido_original.fecha,
                hora_inicio=partido_original.hora_inicio,
                hora_fin=partido_original.hora_fin,
                estado_reserva=partido_original.estado_reserva,
                pista=partido_original.pista,
                club=partido_original.club,
                usuario=request.current_user,  # El usuario que acepta la invitación
                resultado_partido=None  # Inicialmente sin resultado
            )
            
            messages.success(
                request, 
                f'Invitación aceptada correctamente. Se ha creado un nuevo partido para el {partido_original.fecha}.'
            )
            
        except Exception as e:
            # Si hay error al crear el partido, revertir el estado de la invitación
            invitacion.estado = 'pendiente'
            invitacion.save()
            messages.error(request, 'Error al crear el partido. Por favor, inténtalo de nuevo.')
    
    return redirect('home_jugador')


@login_required_custom
@jugador_required
def rechazar_invitacion(request, invitacion_id):
    """
    Rechaza una invitación pendiente
    """
    if request.method == 'POST':
        invitacion = get_object_or_404(
            Invitaciones,
            id=invitacion_id,
            invitado_email=request.current_user.email,
            estado='pendiente'
        )
        
        invitacion.estado = 'rechazada'
        invitacion.save()
        
        messages.success(request, 'Invitación rechazada.')
    
    return redirect('home_jugador')


@login_required_custom
@jugador_required
def crear_invitacion(request):
    """
    Formulario para crear una nueva invitación
    """
    if request.method == 'POST':
        invitado_email = request.POST.get('invitado_email')
        partido_id = request.POST.get('partido_id')
        
        # Validaciones básicas
        if not invitado_email or not partido_id:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('crear_invitacion')
        
        # Verificar que el email del invitado no sea el mismo que el del usuario
        if invitado_email == request.current_user.email:
            messages.error(request, 'No puedes invitarte a ti mismo.')
            return redirect('crear_invitacion')
        
        try:
            partido = Partido.objects.get(id=partido_id, usuario=request.current_user)
        except Partido.DoesNotExist:
            messages.error(request, 'El partido seleccionado no existe o no te pertenece.')
            return redirect('crear_invitacion')
        
        # Verificar que no existe ya una invitación para este partido y email
        if Invitaciones.objects.filter(partido=partido, invitado_email=invitado_email).exists():
            messages.error(request, 'Ya existe una invitación para este usuario en este partido.')
            return redirect('crear_invitacion')
        
        # Verificar que el usuario invitado existe
        try:
            usuario_invitado = Usuario.objects.get(email=invitado_email)
            if usuario_invitado.tipo_usuario.nombre != 'jugador':
                messages.error(request, 'Solo puedes invitar a usuarios de tipo jugador.')
                return redirect('crear_invitacion')
        except Usuario.DoesNotExist:
            messages.error(request, 'No existe un usuario registrado con ese email.')
            return redirect('crear_invitacion')
        
        # Crear la invitación
        Invitaciones.objects.create(
            usuario=request.current_user,
            invitado_email=invitado_email,
            partido=partido,
            estado='pendiente'
        )
        
        messages.success(request, f'Invitación enviada a {invitado_email}.')
        return redirect('home_jugador')
    
    # GET - Mostrar formulario
    # Obtener partidos futuros del usuario para poder invitar
    hoy = date.today()
    partidos_disponibles = Partido.objects.filter(
        usuario=request.current_user,
        fecha__gte=hoy
    ).select_related('club', 'pista').order_by('fecha', 'hora_inicio')
    
    context = {
        'partidos_disponibles': partidos_disponibles,
    }
    
    return render(request, 'usuarios/crear_invitacion.html', context)


@login_required_custom
@jugador_required
def mis_partidos(request):
    """
    Lista todos los partidos del usuario (propios + invitaciones aceptadas)
    """
    usuario = request.current_user
    
    # Partidos creados por el usuario
    partidos_usuario = Partido.objects.filter(usuario=usuario)
    
    # Partidos donde fue invitado y aceptó
    invitaciones_aceptadas = Invitaciones.objects.filter(
        invitado_email=usuario.email,
        estado='aceptada'
    ).values_list('partido_id', flat=True)
    
    partidos_invitado = Partido.objects.filter(id__in=invitaciones_aceptadas)
    
    # Combinar y ordenar
    todos_partidos = (partidos_usuario | partidos_invitado).distinct().select_related(
        'club', 'pista', 'estado_reserva', 'usuario'
    ).order_by('-fecha', '-hora_inicio')
    
    # Separar en próximos y pasados
    hoy = date.today()
    partidos_proximos = todos_partidos.filter(fecha__gte=hoy)
    partidos_pasados = todos_partidos.filter(fecha__lt=hoy)
    
    context = {
        'partidos_proximos': partidos_proximos,
        'partidos_pasados': partidos_pasados,
    }
    
    return render(request, 'usuarios/mis_partidos.html', context)


@login_required_custom
@jugador_required
def detalle_partido(request, partido_id):
    """
    Detalle de un partido específico
    """
    # El usuario puede ver el partido si lo creó o fue invitado y aceptó
    partido = get_object_or_404(Partido, id=partido_id)
    
    # Verificar permisos
    es_creador = partido.usuario == request.current_user
    es_invitado = Invitaciones.objects.filter(
        partido=partido,
        invitado_email=request.current_user.email,
        estado='aceptada'
    ).exists()
    
    if not (es_creador or es_invitado):
        messages.error(request, 'No tienes permisos para ver este partido.')
        return redirect('home_jugador')
    
    # Obtener invitaciones relacionadas
    invitaciones = Invitaciones.objects.filter(partido=partido).select_related('usuario')
    
    context = {
        'partido': partido,
        'invitaciones': invitaciones,
        'es_creador': es_creador,
        'es_invitado': es_invitado,
    }
    
    return render(request, 'usuarios/detalle_partido.html', context)


@login_required_custom
@jugador_required
def crear_partido(request):
    clubs = Club.objects.all()

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        club_id = request.POST.get('club_id')
        pista_id = request.POST.get('pista_id')

        club = get_object_or_404(Club, id=club_id)
        pista = get_object_or_404(Pista, id=pista_id, club=club)
        estado_reserva = EstadoReserva.objects.get(nombre="Pendiente")  # Ajusta si usas otro nombre

        partido = Partido.objects.create(
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            club=club,
            pista=pista,
            estado_reserva=estado_reserva,
            usuario=request.user  # ← aquí estaba mal (antes era `creador`)
        )
        return redirect('home_jugador')

    context = {
        'clubs': clubs,
        'fecha_minima': date.today().isoformat()
    }
    return render(request, 'partidos/crear_partido.html', context)


@require_GET
def obtener_pistas_club(request, club_id):
    try:
        pistas = Pista.objects.filter(club_id=club_id)
        pistas_data = [{'id': pista.id, 'nombre': pista.nombre} for pista in pistas]
        return JsonResponse({'success': True, 'pistas': pistas_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})