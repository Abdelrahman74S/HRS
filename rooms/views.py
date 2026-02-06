from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView , DeleteView
from django.db import transaction
from .models import Room
from .forms import RoomForm, RoomImageFormSet
from rooms.Ispermissions import IsManager
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime
from Reservation.models import Booking

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
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        
        q = self.request.GET.get('q')
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')

        if q:
            queryset = queryset.filter(
                Q(room_number__icontains=q) |
                Q(room_type__name__icontains=q) |
                Q(notes__icontains=q)
            )

        if check_in and check_out:
            try:
                c_in = datetime.strptime(check_in, "%Y-%m-%d").date()
                c_out = datetime.strptime(check_out, "%Y-%m-%d").date()
                
                booked_rooms_ids = Booking.objects.filter(
                    status__in=['confirmed', 'checked_in', 'pending'],
                    check_in_date__lt=c_out,
                    check_out_date__gt=c_in
                ).values_list('room_id', flat=True)
                
                queryset = queryset.exclude(id__in=booked_rooms_ids)
            except ValueError:
                pass 
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['check_in'] = self.request.GET.get('check_in', '')
        context['check_out'] = self.request.GET.get('check_out', '')
        return context

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


# def search(request):
#     q = request.GET.get('q', '')
#     check_in = request.GET.get('check_in')
#     check_out = request.GET.get('check_out')

#     rooms = Room.objects.filter(is_active=True)

#     if q:
#         rooms = rooms.filter(
#             Q(room_number__icontains=q) |
#             Q(room_type__name__icontains=q) |
#             Q(notes__icontains=q)
#         )

#     if check_in and check_out:
#         try:
#             check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
#             check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

#             booked_rooms_ids = Booking.objects.filter(
#                 status__in=['confirmed', 'checked_in', 'pending'],
#                 check_in_date__lt=check_out_date,
#                 check_out_date__gt=check_in_date
#             ).values_list('room_id', flat=True)

#             rooms = rooms.exclude(id__in=booked_rooms_ids)
#         except ValueError:
#             pass

#     return render(request, 'rooms/search.html', {
#         'rooms': rooms,
#         'q': q,
#         'check_in': check_in,
#         'check_out': check_out
#     })