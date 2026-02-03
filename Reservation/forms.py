from django import forms
from .models import Booking, Payment

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'guest', 'room', 'check_in_date', 'check_out_date', 
            'number_of_guests', 'status', 'special_requests'
        ]
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requirements?'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'payment_status', 'transaction_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Enter transaction reference if applicable'}),
        }