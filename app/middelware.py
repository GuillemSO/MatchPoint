from django.shortcuts import redirect
from django.urls import reverse_lazy

class AuthRedirectMiddleware:
    """
    Middleware para manejar redirecciones automáticas
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que no requieren autenticación
        self.public_urls = [
            '/login/',
            '/registro/',
            '/admin/',  # Django admin
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        if request.path == '/' and not request.session.get('usuario_id'):
            return redirect('login')
        
        if request.path == '/login/' and request.session.get('usuario_id'):
            return self.redirect_by_user_type(request)
        
        response = self.get_response(request)
        return response
    
    def redirect_by_user_type(self, request):
        """Redirigir según el tipo de usuario"""
       
        from .usuarios.models import Usuario
        try:
            usuario_id = request.session.get('usuario_id')
            usuario = Usuario.objects.get(id=usuario_id)
            user_type = usuario.tipo_usuario.nombre if usuario.tipo_usuario else None
            
            if user_type == 'jugador':
                return redirect('home')
            elif user_type == 'admin_club':
                return redirect('home_admin_club')
            elif user_type == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('login')
        except:
            request.session.flush()
            return redirect('login')