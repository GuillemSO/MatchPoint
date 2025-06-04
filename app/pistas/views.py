from pyexpat.errors import messages
from rest_framework import viewsets
from .models import Pista
from .serializers import PistaSerializer
from django.views.generic import ListView
from django.shortcuts import redirect
from app.clubs.models import Club
from app.usuarios.models import Usuario
from django.shortcuts import render, redirect
from app.decorators import admin_club_required
from app.tipo_pista.models import TipoPista
from app.estado_pista.models import EstadoPista
from app.pistas.models import Pista
from django.contrib import messages
from django.shortcuts import get_object_or_404



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

@admin_club_required
def pista_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio') 
        estado_pista_id = request.POST.get('estado_pista')
        tipo_pista_radio = request.POST.get('tipo_pista_radio')

        # Crear objeto TipoPista según selección
        if tipo_pista_radio == 'doble':
            tipo_pista = TipoPista.objects.create(doble=True, individual=False)
        else:
            tipo_pista = TipoPista.objects.create(doble=False, individual=True)

        club = Club.objects.get(usuario=request.current_user)

        Pista.objects.create(
            nombre=nombre,
            precio=precio,
            tipo_pista=tipo_pista,
            estado_pista_id=estado_pista_id,
            club=club
        )
        messages.success(request, 'Pista creada correctamente')
        return redirect('home_admin_club')

    estado_pista = EstadoPista.objects.all()
    return render(request, 'pistas/pista_form.html', {
        'estados_pista': estado_pista
    })

@admin_club_required
def pista_update(request, pk):
    pista = get_object_or_404(Pista, pk=pk, club__usuario=request.current_user)

    tipo_pista = pista.tipo_pista  # ya está relacionada
    estados_pista = EstadoPista.objects.all()

    if request.method == 'POST':
        pista.nombre = request.POST.get('nombre')
        pista.precio = request.POST.get('precio')
        estado_pista_id = request.POST.get('estado_pista')
        tipo = request.POST.get('tipo_pista')  # 'individual' o 'doble'

        # Actualizar TipoPista actual
        tipo_pista.individual = (tipo == 'individual')
        tipo_pista.doble = (tipo == 'doble')
        tipo_pista.save()

        pista.estado_pista_id = estado_pista_id
        pista.save()

        messages.success(request, 'Pista actualizada correctamente.')
        return redirect('home_admin_club')

    return render(request, 'pistas/pista_form.html', {
        'pista': pista,
        'tipo_pista': tipo_pista,
        'estados_pista': estados_pista
    })



@admin_club_required
def pista_delete(request, pk):
    pista = get_object_or_404(Pista, pk=pk)

    if pista.club.usuario != request.current_user:
        messages.error(request, "No tienes permiso para eliminar esta pista.")
        return redirect('home_admin_club')

    if request.method == 'POST':
        pista.delete()
        messages.success(request, "Pista eliminada correctamente.")
        return redirect('home_admin_club')

    return render(request, 'pistas/pista_confirm_delete.html', {'pista': pista})
