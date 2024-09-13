from typing import Any
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from .models import Ipconfiguration, Vendorconfiguration , Juniperconfiguration as VendorConfigModel
from .forms import RegistrationIpconfiguration, Vendorconfiguration as VendorConfigForm
from .forms import Vendorconfiguration
from .models import Juniperconfiguration
from .models import ciscoBGPconfiguration
from .models import juniperBGPconfiguration
from .models import MikrotikIpconfiguration
from .models import VendorforSwitchConfiguration
from .models import VlanConfigurationSwitch
from .models import InterfaceConfigurationSwitch
from django.http import StreamingHttpResponse
import yaml
import time
import subprocess
# from django.shortcuts import render, get_object_or_404
import subprocess
from django.core.management.base import BaseCommand
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User





#Create your views here.



#Authentication part


def sign_up(request):
    return render(request, 'dashboard/registration.html') 


def index(request):
    if request.method=="POST":
        user_name=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(request,username=user_name,password=passw)
        if user is not None:
            login(request,user)
            return redirect('/dashboard/')
        else:
            return HttpResponse('Credential does not match')
    return render(request, 'dashboard/index.html')


def logut_page(request):
    logout(request)
    return redirect('/')




# def registration(request):
#     if request.method=="POST":
#         username=request.POST.get('username')
#         mail_address=request.POST.get('email_address')
#         password=request.POST.get('password')
#         confirm_password=request.POST.get('confirm_Password')

#         if password!=confirm_password:
#             return HttpResponse("Wrong Password")
#         else:
#             my_user=User.objects.create_user(username,mail_address,password)
#             my_user.save()
#             return HttpResponseRedirect('/dashboard/')

#         # print(username,mail_address,password,confirm_password)
#     return render(request, 'dashboard/registration.html')

@login_required(login_url='/')
def ip(request):
        
    vendor_instance = None
    if request.method == 'POST':
        vendor_data = Vendorconfiguration.objects.all()
        fm = RegistrationIpconfiguration(request.POST)
        if fm.is_valid():
            vr = fm.cleaned_data['version']
            i_name = fm.cleaned_data['interface_name']
            des=fm.cleaned_data['description']
            i_address = fm.cleaned_data['ip_address']
            mask = fm.cleaned_data['net_mask']
            dn = fm.cleaned_data['vd']
            
            if Ipconfiguration.objects.filter(vlan_id=second_part).exists():
                stud = Ipconfiguration.objects.all()
                return HttpResponseRedirect('/dashboard/ip/')
            else:
                if "." in i_name:
                    parts = i_name.split(".")
                    second_part = ".".join(parts[1:])
                    # i_name = second_part
                    reg = Ipconfiguration(
                        version=vr, interface_name=i_name,vlan_id=second_part, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
                    
                else:
                    reg = Ipconfiguration(
                        version=vr, interface_name=i_name, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
        else:
            fm = RegistrationIpconfiguration(request.POST)

    stud = {
        'object1_data': Ipconfiguration.objects.all(),
        'object2_data': Vendorconfiguration.objects.all(),
    }
    return render(request, 'dashboard/ip.html', stud)

#cisco BGP configuration
@login_required(login_url='/')
def bgp(request):
    if request.method == "POST":
        bgp_ip=request.POST.get('ip_address')
        bgp_remote_ip=request.POST.get('remote_ip_address')
        bgp__as=request.POST.get('as_number')
        bgp_remote_as=request.POST.get('remote_as_number')
    
        reg = ciscoBGPconfiguration(
            ip_address=bgp_ip, remote_ip_address=bgp_remote_ip,as_number=bgp__as,remote_as_number=bgp_remote_as)
        reg.save()
    stud = ciscoBGPconfiguration.objects.all()
    return render(request, 'dashboard/bgp_configuration.html',{'stu':stud})

@login_required(login_url='/')
def home(request):
    stud = User.objects.all()
    return render(request, 'dashboard/home.html',{'stu':stud})

#delete ip configuration
@login_required(login_url='/')
def delete_data(request,id):
    if request.method == 'POST':
        pi=Ipconfiguration.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/ip/')
    

#delete juniper ip configuration
@login_required(login_url='/')
def juniper_ip_data_delete(request,id):
    if request.method == 'POST':
        pi=Juniperconfiguration.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/juniper_ipconfiguration')
    

def my_view(request):
    yaml_file_path = 'DJANO ADMIN PANNEL DASHBOARD/admin_pannel/dashboard/ipaddress.yml'

    with open(yaml_file_path, 'r') as f:
        yaml_data = yaml.load(f)

    context = {
        'hosts': yaml_data,
        'vars': yaml_data,
    }

    return render(request, 'ip.html', {'context': context})




#CONFIGURATION FOR EXECUTION(cisco)


@login_required(login_url='/')
def executionData(request, id):
    file_name = "dashboard/ipadress.yml"

    if request.method == 'POST':
        pi = get_object_or_404(Ipconfiguration, pk=id)
        des=pi.description
        i_address=pi.interface_name
        mask=pi.net_mask
        i_name=pi.interface_name
        try:
            with open(file_name, 'r') as f:
                content = yaml.safe_load(f)

                if content is not None:
                    if isinstance(content, list):
                        content[0]['tasks'][2]['iosxr_config']['lines'].clear()
                        if not content[0]['tasks'][2]['iosxr_config']['lines']:
                            content[0]['tasks'][2]['iosxr_config']['lines'].clear()
                            content[0]['hosts'] = 'router_singapore'
                            content[0]['tasks'][2]['iosxr_config']['lines'].append("description " + des)
                            content[0]['tasks'][2]['iosxr_config']['lines'].append("ipv4 address " + i_address + " " + mask)
                            content[0]['tasks'][2]['iosxr_config']['lines'].append("no shutdown")
                            content[0]['tasks'][2]['iosxr_config']['parents']='interface ' + i_name
                            # with open(file_name, 'w') as f:
                            #     yaml.safe_dump(content, f)
                            # class Command(BaseCommand):
                            #     help="Execute an Ansible playbook"
                                
                            #     def handle():
                            #         ansible_playbook_command=['ansible-playbook','ipadress.yml']
                            #         subprocess.run(ansible_playbook_command,check=True)
                            #         return super().handle()
                            #     handle()
                        else:
                            content[0]['tasks'][2]['iosxr_config']['lines'].clear()
                        
                    elif isinstance(content, dict):
                        content['hosts'] = 'router_singapore'
                    else:
                        print("Error: YAML file contains unexpected data type.")

            if content is not None:
                with open(file_name, 'w') as f:
                    yaml.safe_dump(content, f)
        except Exception as e:
            print(f"An error occurred: {e}")
        

        # Return the JSON response
        # return JsonResponse(response_data)
    
    return HttpResponseRedirect('/dashboard/ip/')

# def executionForCisco(request,id):
#     playbook_output = """
    
#     """
#     playbook_lines = playbook_output.split('\n')
#     context = {'playbook_lines': playbook_lines}

#     return render(request, 'dashboard/execution.html',{'playbook_lines': playbook_lines})

def executionAllForCisco(request):
    playbook_output = """
    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']

    PLAYBOOK: ipadd.yml ************************************************************************************************************
    1 plays in ipadd.yml

    PLAY [cisco_singapore] ********************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/ipadd.yml:7
    ok: [cisco_singapore] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/ipadd.yml:10
    ok: [cisco_singapore] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/ipadd.yml:17
    <14.1.101.248> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.248> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.248> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.248> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [cisco_singapore] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test-",
                    "ipv4 address 50.50.50.1 255.255.255.0",
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface Loopback101"
                ],
                "provider": {
                    "host": "14.1.101.248",
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers

    ============================================

    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']

    PLAYBOOK: jun-ipadd.yml ***************************************************************************************************************
    1 plays in jun-ipadd.yml

    PLAY [cisco_agg] ***********************************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/jun-ipadd.yml:7
    ok: [juniper_agg] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/jun-ipadd.yml:10
    ok: [juniper_agg] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/jun-ipadd.yml:17

    <14.1.101.210> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.210> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.210> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.210> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [cisco_agg] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test",
                    "ipv4 address 60.60.60.1 255.255.255.0",
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface Loopback102”
                ],
                "provider": {
                    "host": "14.1.101.210”,
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers
    ==================================

    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']

    PLAYBOOK: jun-ipadd.yml ***************************************************************************************************************
    1 plays in jun-ipadd.yml

    PLAY [cisco_sng] ***********************************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/jun-ipadd.yml:8
    ok: [juniper_agg] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/jun-ipadd.yml:11
    ok: [juniper_agg] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/jun-ipadd.yml:17

    <14.1.101.250> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.250> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.250> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.250> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [cisco_sng] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test",
                    "ipv4 address 70.70.60.1 255.255.255.0",
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface Loopback103”
                ],
                "provider": {
                    "host": "14.1.101.250”,
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers
    ===================================

    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']

    PLAYBOOK: ipadd.yml ************************************************************************************************************
    1 plays in ipadd.yml

    PLAY [cisco_ccu] ********************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/ipadd.yml:7
    ok: [cisco_ccu] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/ipadd.yml:10
    ok: [cisco_ccu] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/ipadd.yml:17
    <14.1.101.212> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.212> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.212> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.212> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [cisco_singapore] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test-",
                    "ipv4 address 90.90.90.1 255.255.255.0",
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface Loopback105”
                ],
                "provider": {
                    "host": "14.1.101.212”,
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers
    ==============================================

    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg

    PLAYBOOK: mipadd.yml ************************************************************************************************************
    1 plays in mipadd.yml

    PLAY [office_mikrotik] ********************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/mipadd.yml:7
    ok: [office_mikrotik] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/mipadd.yml:10
    ok: [cisco] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/mipadd.yml:17
    <14.1.101.213> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.213> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.213> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.213> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [office_mikrotik] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test-",
                    "ipv4 address 95.95.95.1 255.255.255.0",
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface Loopback106”
                ],
                "provider": {
                    "host": "14.1.101.213”,
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers
    ==============================================

    ansible-playbook [core 2.12.10]
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']

    PLAYBOOK: mipadd.yml ************************************************************************************************************
    1 plays in mipadd.yml

    PLAY [mikrotik_colo] ********************************************************************************************************
    META: ran handlers

    TASK [OBTAIN LOGIN INFORMATION] ************************************************************************************************
    task path: /opt/mipadd.yml:7
    ok: [mikrotik_colo] => {
        "ansible_facts": {
            "creds": {
                "password": "*****",
                "username": "*****"
            }
        },
        "ansible_included_var_files": [
            "/opt/secrets.yml"
        ],
        "changed": false
    }

    TASK [DEFINE PROVIDER] *********************************************************************************************************
    task path: /opt/mipadd.yml:10
    ok: [mikrotik_colo] => {
        "changed": false
    }

    TASK [CONFIGURE INTERFACE SETTINGS] ********************************************************************************************
    task path: /opt/mipadd.yml:17
    <14.1.101.211> using connection plugin ansible.netcommon.network_cli (was local)
    <14.1.101.211> ESTABLISH LOCAL CONNECTION FOR USER: root
    <14.1.101.211> EXEC /bin/sh -c 'echo ~root && sleep 0'
    <14.1.101.211> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp "&& mkdir " echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 " && echo ansible-tmp-1708279601.3553147-10905-137664250313213=" echo /root/.ansible/tmp/ansible-tmp-1708279601.3553147-10905-137664250313213 `" ) && sleep 0'
    redirecting (type: modules) 
    [WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present
    in the running configuration on device
    [WARNING]: ['connection local support for this module is deprecated and will be removed in version 2.14, use connection
    ansible.netcommon.network_cli']
    changed: [office_mikrotik] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "lines": [
                    "description test-",
                    "ipv4 address 85.85.85.1 255.255.255.0”,
                    "no shutdown"
                ],
                "match": "line",
                "parents": [
                    "interface ether7”
                ],
                "provider": {
                    "host": "14.1.101.211”,
                    "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "port": null,
                    "ssh_keyfile": null,
                    "timeout": null,
                    "transport": "cli",
                    "username": "iot"
                },
                "replace": "line",
                "src": null
            }
        }
    }
    META: ran handlers
    META: ran handlers
    ===========================================================
    changed: [juniper_agg]
    
    PLAY RECAP ************************************************

    juniper_agg                : ok=3  changed=1  unreachable=0

    changed: [juniper_sng]

    PLAY RECAP ************************************************

    juniper_sng                : ok=3  changed=1  unreachable=0

    changed: [cisco_singapore]
    
    PLAY RECAP ************************************************

    cisco_singapore            : ok=3  changed=1  unreachable=0

    changed: [cisco_ccu]
    
    PLAY RECAP ************************************************

    cisco_ccu                  : ok=3  changed=1  unreachable=0

    changed: [office_mikrotik]
    
    PLAY RECAP ************************************************

    office_mikrotik            : ok=3  changed=1  unreachable=0

    changed: [mikrotik_colo]

    PLAY RECAP ************************************************

    mikrotik_colo              : ok=3  changed=1  unreachable=0

    Playbook execution time: 0 minutes and 7 seconds
    """
    playbook_lines = playbook_output.split('\n')
    context = {'playbook_lines': playbook_lines}
    return render(request, 'dashboard/executionAllForCisco.html', {'playbook_lines': playbook_lines})
    


#CONFIGURATION FOR EXECUTION(juniper)
@login_required(login_url='/')
def juniperIpConfiguration(request):
    vendor_instance = None
    if request.method == 'POST':
        vendor_data = Vendorconfiguration.objects.all()
        fm = RegistrationIpconfiguration(request.POST)
        if fm.is_valid():
            vr = fm.cleaned_data['version']
            i_name = fm.cleaned_data['interface_name']
            des = fm.cleaned_data['description']
            i_address = fm.cleaned_data['ip_address']
            mask = fm.cleaned_data['net_mask']
            dn = fm.cleaned_data['vd']
            
            if Juniperconfiguration.objects.filter(vlan_id=second_part).exists():
                stud = Juniperconfiguration.objects.all()
                return render(request, 'dashboard/ip.html', {'stu': stud})
            else:
                if "." in i_name:
                    parts = i_name.split(".")
                    second_part = ".".join(parts[1:])
                    # i_name = second_part
                    reg = Juniperconfiguration(
                        version=vr, interface_name=i_name,vlan_id=second_part, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
                    
                else:
                    reg = Juniperconfiguration(
                        version=vr, interface_name=i_name,vlan_id=second_part, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
            
        else:
            fm = Juniperconfiguration(request.POST)

    stud = {
        'object1_data': Juniperconfiguration.objects.all(),
        'object2_data': Vendorconfiguration.objects.all(),
    }
    
    return render(request, 'dashboard/juniper_ipconfiguration.html',stud)



def juniperIpConfigurationExecution(request):
    return render(request, 'dashboard/juniperIpConfigurationExecution.html')


#juniper BGP configuration
def juniperBGPConfiguration(request):
    if request.method == "POST":
        bgp_ip=request.POST.get('ip_address')
        bgp_remote_ip=request.POST.get('remote_ip_address')
        bgp__as=request.POST.get('as_number')
        bgp_remote_as=request.POST.get('remote_as_number')
    
        reg = juniperBGPconfiguration(
            ip_address=bgp_ip, remote_ip_address=bgp_remote_ip,as_number=bgp__as,remote_as_number=bgp_remote_as)
        reg.save()
    stu = juniperBGPconfiguration.objects.all()
    return render(request, 'dashboard/juniperBGPConfiguration.html',{'stu': stu})

# mikrotik ip configuration
def mikrotik_ipconfiguration(request):
    vendor_instance = None
    if request.method == 'POST':
        vendor_data = Vendorconfiguration.objects.all()
        fm = RegistrationIpconfiguration(request.POST)
        if fm.is_valid():
            vr = fm.cleaned_data['version']
            i_name = fm.cleaned_data['interface_name']
            des=fm.cleaned_data['description']
            i_address = fm.cleaned_data['ip_address']
            mask = fm.cleaned_data['net_mask']
            dn = fm.cleaned_data['vd']
            
            if MikrotikIpconfiguration.objects.filter(interface_name=i_name).exists():
                stud = MikrotikIpconfiguration.objects.all()
                return HttpResponseRedirect('/dashboard/ip/')
            else:
                if "." in i_name:
                    parts = i_name.split(".")
                    second_part = ".".join(parts[1:])
                    # i_name = second_part
                    reg = MikrotikIpconfiguration(
                        version=vr, interface_name=i_name,vlan_id=second_part, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
                    
                else:
                    reg = MikrotikIpconfiguration(
                        version=vr, interface_name=i_name, description=des, ip_address=i_address, net_mask=mask,vd=dn)
                    reg.save()
                    file_name = "dashboard/ipadress.yml"
        else:
            fm = MikrotikIpconfiguration(request.POST)

    stud = {
        'object1_data': MikrotikIpconfiguration.objects.all(),
        'object2_data': Vendorconfiguration.objects.all(),
    }
    return render(request, 'dashboard/mikrotik_ipconfiguration.html',stud)

#vendor authentication part
@login_required(login_url='/')
def vendorConfiguration(request):
    if request.method == "POST":
        vn=request.POST.get('vendor')
        d_name=request.POST.get('device_name')
    
        reg = Vendorconfiguration(
            vendor=vn, device_name=d_name)
        reg.save()
    stud = Vendorconfiguration.objects.all() 
    return render(request, 'dashboard/vendor.html', {'stu': stud})

def delete_vendor_data(request,id):
    if request.method == 'POST':
        pi=Vendorconfiguration.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/vendor/')


def executealldevices(request):
    return render(request, 'dashboard/executealldevices.html')
# def execute_configuration(request,id):
#     file_name = "dashboard/ipadress.yml"
#     # post = Ipconfiguration.objects.get(id=id)
#     # interface_name=post.interface_name
#     with open(file_name, 'r') as f: 
#         content = yaml.safe_load(f)
#     descrip=content[0]['tasks'][2]['iosxr_config']['lines'][0].split()
#     ip_add=content[0]['tasks'][2]['iosxr_config']['lines'][1].split()
    
    
#     print(ip_add[2])
#     return render(request, 'dashboard/execute_data.html', {'post': interface_name})
    
# execute_configuration()





#configuration for switches

def vendorforSwitchConfiguration(request):
    if request.method == "POST":
        vn=request.POST.get('vendor')
        d_name=request.POST.get('device_name')
    
        reg = VendorforSwitchConfiguration(
            vendor=vn, device_name=d_name)
        reg.save()
    stud = VendorforSwitchConfiguration.objects.all()
    return render(request, 'dashboard/vendorforSwitchConfiguration.html',{'stu':stud})

def delete_switch_vendor_data(request,id):
    if request.method == 'POST':
        pi=VendorforSwitchConfiguration.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/switch/vendor')
    


def vlanforSwitch(request):
    vendor_data = VendorforSwitchConfiguration.objects.all()
    if request.method == "POST":
        vn=request.POST.get('vendor_name')
        d_name=request.POST.get('device_name')
        v_id=request.POST.get('vlan_id')
        des=request.POST.get('description')
        if VlanConfigurationSwitch.objects.filter(vlan_id=v_id).exists():
            stud = VlanConfigurationSwitch.objects.all()
            return HttpResponseRedirect('/dashboard/switch/createVlan')
        else:
            reg = VlanConfigurationSwitch(
                vendor_name=vn, device_name=d_name, vlan_id=v_id, description=des)
            reg.save()
    
    else:
        fm = VlanConfigurationSwitch(request.POST)

    stud = {
        'object1_data': VlanConfigurationSwitch.objects.all(),
        'object2_data': VendorforSwitchConfiguration.objects.all(),
    }
    return render(request, 'dashboard/vlanforSwitch.html',stud)

@login_required(login_url='/')
def delete_switch_vlan_data(request,id):
    if request.method == 'POST':
        pi=VlanConfigurationSwitch.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/switch/vlan')
    
def interfaceConfigureForSwitch(request):
    vendor_data = VendorforSwitchConfiguration.objects.all()
    if request.method == "POST":
        d_name=request.POST.get('device_name')
        i_name=request.POST.get('interface_name')
        v_id=request.POST.get('vlan_id')
        mode=request.POST.get('mode')
        if InterfaceConfigurationSwitch.objects.filter(interface_name=i_name).exists():
            stud = InterfaceConfigurationSwitch.objects.all()
            return HttpResponseRedirect('/dashboard/switch/createVlan')
        else:
            reg = InterfaceConfigurationSwitch(
                device_name=d_name, interface_name=i_name, vlan_id=v_id, mode=mode)
            reg.save()
    
    else:
        fm = InterfaceConfigurationSwitch(request.POST)

    stud = {
        'object1_data': InterfaceConfigurationSwitch.objects.all(),
        'object2_data': VendorforSwitchConfiguration.objects.all(),
    }
    return render(request,'dashboard/interfaceSwitch.html',stud)

def delete_switch_interface_data(request,id):
    if request.method == 'POST':
        pi=InterfaceConfigurationSwitch.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/switch/interface_configuration')





    
    



