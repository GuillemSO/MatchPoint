from rest_framework import viewsets
from .models import Club
from .serializers import ClubSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from app.usuarios.models import Usuario
from django.http import HttpResponseForbidden

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'

class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'

class ClubCreateView(CreateView):
    model = Club
    template_name = 'clubs/club_form.html'
    fields = ['nombre', 'direccion', 'telefono', 'email_contacto']  
    success_url = reverse_lazy('club-list')

    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return redirect("login")

        usuario = Usuario.objects.get(id=usuario_id)
        if not usuario.tipo_usuario or usuario.tipo_usuario.nombre != "Administrador":
            return HttpResponseForbidden("Solo los administradores pueden crear clubes.")
        
        self.usuario = usuario
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.usuario  # asignar el usuario creador
        return super().form_valid(form)

class ClubUpdateView(UpdateView):
    model = Club
    template_name = 'clubs/club_form.html'
    fields = ['nombre', 'direccion', 'telefono', 'email_contacto']
    success_url = reverse_lazy('home_admin_club')

    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        self.club = self.get_object()
        if not usuario_id or self.club.usuario.id != usuario_id:
            return HttpResponseForbidden("No tienes permiso.")
        return super().dispatch(request, *args, **kwargs)

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'
    success_url = reverse_lazy('home_admin_club')

    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        self.club = self.get_object()
        if not usuario_id or self.club.usuario.id != usuario_id:
            return HttpResponseForbidden("No tienes permiso.")
        return super().dispatch(request, *args, **kwargs)

