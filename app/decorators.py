from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

def login_required_custom(view_func):
    """
    Decorador personalizado que verifica si el usuario está logueado usando sessions
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # IMPORTACIÓN TARDÍA - dentro del decorador
        from .usuarios.models import Usuario
        
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            # Agregar el usuario al request para fácil acceso
            request.current_user = usuario
        except Usuario.DoesNotExist:
            request.session.flush()
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(*allowed_roles):
    """
    Decorador que verifica el tipo de usuario
    Roles disponibles: 'manager', 'admin_club', 'jugador'
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # IMPORTACIÓN TARDÍA - dentro del decorador
            from .usuarios.models import Usuario
            
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return redirect('login')
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                user_type = usuario.tipo_usuario.nombre if usuario.tipo_usuario else None
                
                if user_type not in allowed_roles:
                    messages.error(request, 'No tienes permisos para acceder a esta página.')
                    # Redirigir según el tipo de usuario
                    if user_type == 'jugador':
                        return redirect('home')
                    elif user_type == 'admin_club':
                        return redirect('home_admin_club')
                    elif user_type == 'manager':
                        return redirect('manager_dashboard')
                    else:
                        return redirect('login')
                
                # Agregar el usuario al request
                request.current_user = usuario
                        
            except Usuario.DoesNotExist:
                request.session.flush()
                return redirect('login')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def manager_required(view_func):
    """Decorador específico para manager"""
    return role_required('manager')(view_func)


def admin_club_required(view_func):
    """Decorador específico para admin_club"""
    return role_required('admin_club')(view_func)


def jugador_required(view_func):
    """Decorador específico para jugador"""
    return role_required('jugador')(view_func)


def admin_club_or_manager_required(view_func):
    """Decorador para admin_club o manager"""
    return role_required('admin_club', 'manager')(view_func)