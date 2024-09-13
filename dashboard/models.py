from django.db import models

# Create your models here.

class Vendorconfiguration(models.Model):
    vendor = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)
    

class Ipconfiguration(models.Model):
    interface_name = models.CharField(max_length=100)
    vlan_id = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True)
    ip_address = models.CharField(max_length=100)
    net_mask = models.CharField(max_length=100)
    vd = models.CharField(max_length=100)
    
class Juniperconfiguration(models.Model):
    interface_name = models.CharField(max_length=100)
    vlan_id = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True)
    ip_address = models.CharField(max_length=100)
    net_mask = models.CharField(max_length=100)
    vd = models.CharField(max_length=100)
    
    

class ciscoBGPconfiguration(models.Model):
    ip_address = models.CharField(max_length=100)
    remote_ip_address = models.CharField(max_length=100)
    as_number = models.CharField(max_length=100)
    remote_as_number = models.CharField(max_length=100)
    
class juniperBGPconfiguration(models.Model):
    ip_address = models.CharField(max_length=100)
    remote_ip_address = models.CharField(max_length=100)
    as_number = models.CharField(max_length=100)
    remote_as_number = models.CharField(max_length=100)
    
class MikrotikIpconfiguration(models.Model):
    interface_name = models.CharField(max_length=100)
    vlan_id = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True)
    ip_address = models.CharField(max_length=100)
    net_mask = models.CharField(max_length=100)
    vd = models.CharField(max_length=100)
    
class VendorforSwitchConfiguration(models.Model):
    vendor = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)

class VlanConfigurationSwitch(models.Model):
    vendor_name = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100,null=True)
    vlan_id = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)
    
class InterfaceConfigurationSwitch(models.Model):
    device_name = models.CharField(max_length=100)
    interface_name = models.CharField(max_length=100,null=True)
    vlan_id = models.CharField(max_length=100,null=True)
    mode = models.CharField(max_length=100,null=True)
    

  
