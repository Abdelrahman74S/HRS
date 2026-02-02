from django import forms
from .models import Room, RoomType, RoomImage
from django.forms import inlineformset_factory

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'description', 'base_price', 'max_occupancy', 
        'bed_type', 'size_sqm', 'image', 'amenities', 'is_active']
        
        widgets = {
            'amenities': forms.CheckboxSelectMultiple(), 
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'floor', 'status', 'is_active', 'pricing_override', 'notes']
        
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'أي ملاحظات عن حالة الغرفة...'}),
        }

class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ['image', 'is_primary', 'caption']


RoomImageFormSet = inlineformset_factory(
    Room, 
    RoomImage, 
    form=RoomImageForm, 
    extra=3,
    can_delete=True
)