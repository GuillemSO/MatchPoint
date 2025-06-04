from pyexpat.errors import messages
from rest_framework import viewsets
from .models import Club
from .serializers import ClubSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from app.usuarios.models import Usuario
from django.http import HttpResponseForbidden
from app.decorators import admin_club_required, manager_required, admin_club_or_manager_required
from django.contrib import messages  # Importación correcta


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


@manager_required
def club_list_manager(request):
    """Lista de todos los clubes - Solo para managers"""
    clubs = Club.objects.all()
    return render(request, 'clubs/club_list.html', {'clubs': clubs})


@admin_club_required
def club_list_admin(request):
    """Lista del club del admin - Solo su club"""
    try:
        club = Club.objects.get(usuario=request.current_user)
        clubs = [club]  # Solo su club
    except Club.DoesNotExist:
        clubs = []
    return render(request, 'clubs/club_list.html', {'clubs': clubs})


@admin_club_or_manager_required
def club_detail(request, pk):
    """Detalle del club"""
    club = get_object_or_404(Club, pk=pk)
    
    # Si es admin_club, verificar que sea su club
    if (hasattr(request, 'current_user') and 
        request.current_user.tipo_usuario.nombre == 'admin_club' and
        club.usuario != request.current_user):
        messages.error(request, 'No tienes permisos para ver este club.')
        return redirect('home_admin_club')
    
    return render(request, 'clubs/club_detail.html', {'club': club})


def club_create(request):
    """Crear club - Solo admin_club"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email_contacto = request.POST.get('email_contacto')
        usuario_id = request.POST.get('usuario')
        
        # Validar que se seleccionó un usuario
        if not usuario_id:
            messages.error(request, 'Debes seleccionar un usuario responsable.')
            usuarios = Usuario.objects.all()
            return render(request, 'clubs/club_form.html', {'usuarios': usuarios})
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            Club.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email_contacto=email_contacto,
                usuario=usuario
            )
            messages.success(request, 'Club creado correctamente')
            return redirect('club-list')  
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario seleccionado no existe.')
    
    usuarios = Usuario.objects.all()
    return render(request, 'clubs/club_form.html', {'usuarios': usuarios})


@admin_club_required
def club_update(request, pk):
    """Actualizar club - Solo el admin propietario"""
    club = get_object_or_404(Club, pk=pk)
  
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email_contacto = request.POST.get('email_contacto')
        usuario_id = request.POST.get('usuario')
        
        if not usuario_id:
            messages.error(request, 'Debes seleccionar un usuario responsable.')
            usuarios = Usuario.objects.all()
            return render(request, 'clubs/club_form.html', {
                'club': club, 
                'usuarios': usuarios
            })
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            club.nombre = nombre
            club.direccion = direccion
            club.telefono = telefono
            club.email_contacto = email_contacto
            club.usuario = usuario
            club.save()
            messages.success(request, 'Club actualizado correctamente')
            return redirect('club-list')  # Cambiar por tu URL de lista de clubes
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario seleccionado no existe.')
    
    # Obtener todos los usuarios para el select
    usuarios = Usuario.objects.all()
    return render(request, 'clubs/club_form.html', {
        'club': club, 
        'usuarios': usuarios
    })


@admin_club_required
def club_delete(request, pk):
    """Eliminar club - Solo el admin propietario"""
    club = get_object_or_404(Club, pk=pk)
    
    # Verificar que sea el propietario
    if club.usuario != request.current_user:
        messages.error(request, 'No tienes permisos para eliminar este club.')
        return redirect('home_admin_club')
    
    if request.method == 'POST':
        club.delete()
        messages.success(request, 'Club eliminado correctamente')
        return redirect('home_admin_club')
    
    return render(request, 'clubs/club_confirm_delete.html', {'club': club})