from django import forms
from .models import Category, Microgreen, WholesaleInquiry


class WholesaleInquiryForm(forms.ModelForm):
    class Meta:
        model = WholesaleInquiry
        fields = [
            'chef_name',
            'role_title',
            'establishment_name',
            'email',
            'phone_whatsapp',
            'region',
            'inquiry_type',
            'selected_varieties_summary',
            'estimated_weekly_volume',
            'preferred_delivery_days',
            'culinary_notes',
        ]
        widgets = {
            'chef_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Chef Jone Vuki',
                'class': 'form-input',
            }),
            'role_title': forms.TextInput(attrs={
                'placeholder': 'e.g., Executive Chef / Sous Chef / F&B Director',
                'class': 'form-input',
            }),
            'establishment_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Likuliku Lagoon Resort / Sails @ Denarau / M/Y Fiji Siren',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'chef@resortfiji.com',
                'class': 'form-input',
            }),
            'phone_whatsapp': forms.TextInput(attrs={
                'placeholder': '+679 999 0000 (WhatsApp enabled)',
                'class': 'form-input',
            }),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'inquiry_type': forms.Select(attrs={'class': 'form-select'}),
            'selected_varieties_summary': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Click "+ Add to Inquiry Tray" on any variety above, or list your desired microgreens here...',
                'class': 'form-textarea',
                'id': 'id_selected_varieties_summary',
            }),
            'estimated_weekly_volume': forms.TextInput(attrs={
                'placeholder': 'e.g., 25 punnets + 4 live trays per week',
                'class': 'form-input',
            }),
            'preferred_delivery_days': forms.TextInput(attrs={
                'placeholder': 'e.g., Tuesday & Friday morning before 9:30 AM',
                'class': 'form-input',
            }),
            'culinary_notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell us about your upcoming degustation menu, garnish needs, or custom seed requests...',
                'class': 'form-textarea',
            }),
        }


class MicrogreenStudioForm(forms.ModelForm):
    class Meta:
        model = Microgreen
        fields = [
            'name',
            'scientific_name',
            'category',
            'primary_image',
            'tagline',
            'description',
            'flavor_profile',
            'intensity_level',
            'texture_notes',
            'culinary_pairings',
            'chef_serving_tip',
            'availability_status',
            'grow_cycle_days',
            'lead_time_notice',
            'price_punnet_fjd',
            'punnet_weight_grams',
            'price_tray_fjd',
            'tray_size_label',
            'nutritional_highlights',
            'storage_instructions',
            'shelf_life_days',
            'is_featured',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Red Garnet Amaranth'}),
            'scientific_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Amaranthus tricolor'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'primary_image': forms.ClearableFileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Vivid crimson stems with a sweet earthy beet finish'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Describe the visual impact on the plate, origin, and why chefs love this variety...'}),
            'flavor_profile': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Earthy Beetroot, Sweet Mineral, Clean Finish'}),
            'intensity_level': forms.Select(attrs={'class': 'form-select'}),
            'texture_notes': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Delicate velvety cotyledons with crisp micro-stems'}),
            'culinary_pairings': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Fijian Kokoda, Seared Yellowfin Tuna, Goat Cheese Tart, Duck Breast'}),
            'chef_serving_tip': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plate dry with precision tweezers right before pass.'}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'grow_cycle_days': forms.NumberInput(attrs={'class': 'form-input', 'min': 3, 'max': 45}),
            'lead_time_notice': forms.TextInput(attrs={'class': 'form-input'}),
            'price_punnet_fjd': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.50'}),
            'punnet_weight_grams': forms.TextInput(attrs={'class': 'form-input'}),
            'price_tray_fjd': forms.NumberInput(attrs={'class': 'form-input', 'step': '1.00'}),
            'tray_size_label': forms.TextInput(attrs={'class': 'form-input'}),
            'nutritional_highlights': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'storage_instructions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'shelf_life_days': forms.NumberInput(attrs={'class': 'form-input', 'min': 2, 'max': 21}),
        }
