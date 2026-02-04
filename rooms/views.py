from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView , DeleteView
from django.db import transaction
from .models import Room
from .forms import RoomForm, RoomImageFormSet
from rooms.Ispermissions import IsManager
from django.db.models import Q
from django.shortcuts import render

class RoomCreateView(IsManager, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room_list')  

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = RoomImageFormSet(self.request.POST, self.request.FILES)
        else:
            data['formset'] = RoomImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)
        return super().form_valid(form)
    

class RoomUpdateView(IsManager, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room_list')  
    slug_field = 'slug' 
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = RoomImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['formset'] = RoomImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)
    

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10 


class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'
    

class RoomDeleteView(IsManager, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:room_list')  
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


def search(request):
    q = request.GET.get('q', '')
    if q:
        rooms = Room.objects.filter(
            Q(room_number__icontains=q) | 
            Q(room_type__name__icontains=q) | 
            Q(notes__icontains=q)
        ).distinct()
    else:
        # rooms = Room.objects.all()
        rooms = Room.objects.none()

    return render(request, 'rooms/search.html', {
    # return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'query': q
    })