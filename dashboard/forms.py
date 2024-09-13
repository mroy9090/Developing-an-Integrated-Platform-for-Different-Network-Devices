from django.core import validators
from django import forms
from .models import Ipconfiguration
from .models import Vendorconfiguration

class RegistrationIpconfiguration(forms.ModelForm):
    class Meta:
        model=Ipconfiguration
        fields=['id', 'version', 'interface_name','description', 'ip_address', 'net_mask', 'vd']
        
        
# class Vendorconfiguration(forms.ModelForm):
#     class Meta:
#         model=Vendorconfiguration
#         fields=['id', 'vendor', 'device_name']