from django import forms
from .models import Booking, Payment

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'check_in_date', 
            'check_out_date', 
            'number_of_guests', 
            'special_requests'
        ]
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'class': 'form-input', 'placeholder': 'Any special requirements?'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1, 'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'payment_status', 'transaction_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Enter transaction reference if applicable'}),
        }