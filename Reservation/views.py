from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Booking , Payment
from .forms import BookingForm , PaymentForm
from rooms.models import Room
from Reservation.Ispermissions import IsGuest
from rooms.Ispermissions import IsManager

class BookingCreateView(IsGuest, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/booking_form.html'
    success_url = reverse_lazy('reservations:my_bookings')

    def form_valid(self, form):
        room = get_object_or_404(Room, slug=self.kwargs['room_slug'])
        check_in = form.cleaned_data.get('check_in_date')
        check_out = form.cleaned_data.get('check_out_date')

        overlapping_bookings = Booking.objects.filter(
            room=room,
            status__in=['confirmed', 'checked_in', 'pending'],
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        ).exists()

        if overlapping_bookings:
            messages.error(self.request, "Sorry, this room is already booked for the selected dates.")
            return self.form_invalid(form)

        form.instance.guest = self.request.user
        form.instance.room = room
        messages.success(self.request, "Your booking request has been created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, slug=self.kwargs['room_slug'])
        return context

class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'reservations/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.user_type == 'M':
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)
    

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'reservations/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.user_type == 'M':
            return Booking.objects.all()

        return Booking.objects.filter(guest=user)

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You do not have permission to view this booking."
        )
        return redirect('reservations:my_bookings')


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'reservations/booking_confirm_delete.html'
    success_url = reverse_lazy('reservations:my_bookings')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.user_type == 'M':
            return Booking.objects.all()
        
        return Booking.objects.filter(
            guest=self.request.user,
            status='pending'
        )

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "The booking has been cancelled successfully."
        )
        return super().delete(request, *args, **kwargs)


class CreatePaymentView(IsGuest,CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'reservations/create_payment.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['booking'] = get_object_or_404(Booking, pk=self.kwargs['booking_id'])
        
        return context
    

    def form_valid(self, form):
        booking = get_object_or_404(Booking, pk=self.kwargs['booking_id'])
        
        form.instance.reservation = booking
        form.instance.amount = booking.total_price
        form.instance.payment_status = 'completed' 
        
        booking.status = 'confirmed'
        booking.save()
        
        messages.success(self.request, "Payment successful and booking confirmed!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reservations:my_bookings')

def check_in_guest(request, booking_id):
    if not (request.user.is_staff or request.user.user_type == 'M'):
        messages.error(request, "Access denied.")
        return redirect('reservations:my_bookings')
            
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.status != 'confirmed':
        messages.error(request, "Cannot check-in. The booking must be confirmed (Paid) first.")
        return redirect('reservations:booking_detail', pk=booking.pk)
    
    booking.status = 'checked_in'
    booking.checked_in_by = request.user
    booking.save()
    
    booking.room.status = 'O' 
    booking.room.save()
    
    messages.success(request, f"Guest checked-in to room {booking.room.room_number}.")
    return redirect('reservations:booking_detail', pk=booking.pk)

def check_out_guest(request, booking_id):
    if not (request.user.is_staff or request.user.user_type == 'M'):
        messages.error(request, "You are not allowed to perform this action.")
        return redirect('reservations:my_bookings')
            
    booking = get_object_or_404(Booking, pk=booking_id)
    
    booking.status = 'checked_out'
    booking.checked_out_by = request.user
    booking.save()
    
    booking.room.status = 'C'  
    booking.room.save()
    
    messages.success(
        request,
        f"Guest has been successfully checked out from room {booking.room.room_number}."
    )
    return redirect('reservations:booking_detail', pk=booking.pk)
