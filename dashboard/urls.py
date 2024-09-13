#dashboard URL configuration


from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard/', views.home, name='dashboard'),



    #authentication
    # path('registration', views.registration, name='registration'),
    path('logout', views.logut_page, name='logout'),






    # cisco configuration part
    path('dashboard/ip/', views.ip, name='ip'),
    path('dashboard/bgp_configuration/', views.bgp, name='bgp_configuration'),
    path('dashboard/delete/<int:id>/', views.delete_data, name='delete_data'),
    path('dashboard/execute/<int:id>/', views.executionData, name='executionData'),
    # since excution data is working right now
    # path('dashboard/execute/<int:id>/', views.executionForCisco, name='executionData'),
    
    # cisco configuration execution all
    path('dashboard/execute/', views.executionAllForCisco, name='executionAllForCisco'),
    
    
     
     
     
     
     
     
    #junipert configuration part
    path('dashboard/juniper_ipconfiguration/', views.juniperIpConfiguration, name='juniperIpConfiguration'),
    path('dashboard/juniper/bgp_configuration/', views.juniperBGPConfiguration, name='juniperBGPConfiguration'),
    path('dashboard/juniper/delete/<int:id>/', views.juniper_ip_data_delete, name='juniper_ip_data_delete'),
    path('dashboard/juniper_ipconfiguration/execute/', views.juniperIpConfigurationExecution, name='juniperIpConfigurationExecution'),
    
    #mikrotik configuration part
    path('dashboard/mikrotik_ipconfiguration/', views.mikrotik_ipconfiguration, name='mikrotik_ipconfiguration'),
    
    
    #Vendor configuration
    path('dashboard/vendor/', views.vendorConfiguration, name='ip'),
    path('dashboard/vendor/delete/<int:id>/', views.delete_vendor_data, name='delete_vendor_data'),
    
    
    
    
    
    #execution configuration
    # path('dashboard/vendor/execute/<int:id>/', views.delete_vendor_data, name='delete_vendor_data'),
    
    
    
    path('dashboard/executealldevices/', views.executealldevices, name='executealldevices'),
    
    
    
    
    
    #configuration at switches
    
    path('dashboard/switch/vendor', views.vendorforSwitchConfiguration, name='vendorforSwitchConfiguration'),
    path('dashboard/switch/vendor/delete/<int:id>/', views.delete_switch_vendor_data, name='delete_switch_vendor_data'),
    path('dashboard/switch/vlan', views.vlanforSwitch, name='vlanforSwitch'),
    path('dashboard/switch/vlan/delete/<int:id>/', views.delete_switch_vlan_data, name='delete_switch_vlan_data'),
    path('dashboard/switch/interface_configuration', views.interfaceConfigureForSwitch, name='interfaceConfigureForSwitch'),
    path('dashboard/switch/interface/delete/<int:id>/', views.delete_switch_interface_data, name='delete_switch_interface_data'),
    
]
