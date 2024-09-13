from django.contrib import admin
from .models import Ipconfiguration
from .models import Vendorconfiguration
# from .models import Juniperconfiguration
# Register your models here.

admin.site.register(Ipconfiguration)
admin.site.register(Vendorconfiguration)
# admin.site.register(Juniperconfiguration)
# class IpconfigurationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'version', 'interface_name','description', 'ip_address', 'net_mask')

