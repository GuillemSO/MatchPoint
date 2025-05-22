from rest_framework import viewsets
from .models import Pista
from .serializers import PistaSerializer
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Pista
from app.clubs.models import Club
from app.usuarios.models import Usuario
from django.shortcuts import render, redirect
from .forms import PistaForm
from .models import Pista
from django.contrib.auth.decorators import login_required
from app.clubs.models import Club

class PistaViewSet(viewsets.ModelViewSet):
    queryset = Pista.objects.all()
    serializer_class = PistaSerializer


class PistaListView(ListView):
    model = Pista
    template_name = 'pistas/pista_list.html'
    context_object_name = 'pistas'

    def get_queryset(self):
        usuario_id = self.request.session.get("usuario_id")
        if not usuario_id:
            return Pista.objects.none()
        usuario = Usuario.objects.get(id=usuario_id)
        return Pista.objects.filter(club__usuario=usuario)



def crear_pista(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect('home')  # o redirigir al login

    usuario = Usuario.objects.get(id=usuario_id)

    if usuario.tipo_usuario.nombre != 'admin_club':
        return redirect('home')

    club = Club.objects.get(usuario=request.user)

    if not club:
        return redirect('home_admin_club')

    if request.method == 'POST':
        form = PistaForm(request.POST)
        if form.is_valid():
            pista = form.save(commit=False)
            pista.club = club
            pista.save()
            return redirect('home_admin_club')
    else:
        form = PistaForm()

    return render(request, 'pistas/crear_pista.html', {'form': form})
