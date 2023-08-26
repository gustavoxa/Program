import requests
import json
import pandas as pd
from pprint import pprint
import pickle 
class Servicio:
    Usuario = " "
    Contrasenia = " "
    Ip = " "
    def __init__(self,usuario,contrasenia,ip):
        self.Usuario = usuario
        self.Contrasenia = contrasenia
        self.Ip = ip
        self.port = "443"
        self.headers = {
                "Accept" : "application/yang-data+json", 
                "Content-Type" : "application/yang-data+json", 
        }

# Creación de Interfaces de loopback
    def Interfaces_loopback(self,nombre_loopback,dir_ip,mascara):
        module = "ietf-interfaces:interfaces"
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}/interface={nombre_loopback}"
        payload = {
            "interface": [
                {
                    "name": nombre_loopback,
                    "description": "Adding loopback10000 - changed",
                    "type": "iana-if-type:softwareLoopback",
                    "enabled": "true",
                    "ietf-ip:ipv4": {
                        "address": [
                                {
                                    "ip": dir_ip,
                                    "netmask": mascara
            	                }
                            ]
                    }
                }
            ]
         }
        self.Peticiones_put(url,payload)
# Creación de Vlans
   
    def Vlan_interface(self,nombre_vlan,ip_vlan,mascara_vlan):
        module = "ietf-interfaces:interfaces"
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}/interface={nombre_vlan}"
        payload = {
            "ietf-interfaces:interface": {
                "name": nombre_vlan,
                "type": "iana-if-type:l3ipvlan",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": ip_vlan,
                            "netmask": mascara_vlan
                        }
                    ]
                }
        
            }
         }
        print(url)
        self.Peticiones_put(url,payload)

# Asignación de IP

    def interface(self,interfaceurl,interface,ip,mascara):
        module = "ietf-interfaces:interfaces"
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}/interface={interfaceurl}"
        payload = {
            "ietf-interfaces:interface": {
                "name": interface,
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": ip,
                            "netmask": mascara
                        }
                    ]
                }
        
            }
         }
        print(url)
        print(payload)
        self.Peticiones_put(url,payload)

    
# Cambiar nombre 
    def Nombre_dispositivo(self,nombre):
         module = "Cisco-IOS-XE-native:native/hostname"
         url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"        
         payload = {
             "hostname":
                    nombre
         }
         self.Peticiones_put(url,payload)
#Crear usuarios
    def Usuarios(self,user,password):
        module = 'Cisco-IOS-XE-native:native/username'
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"    
        payload = {
            "Cisco-IOS-XE-native:username": 
            [
                {
                    "name": user,
                    "privilege": 15,
                      "secret": {
                          "encryption": "9",
                          "secret": "$9$nbucXlXs.KZwHU$N1yYgE2D3Jnzdn.nljSAZHgjboFcfEEn2q5lmYBRJT."
                          } 
                 }
             ]
         }
        self.Peticiones_patch(url,payload)
#Configurar DHCP
    def Configuracion_DHCP(self,ipminexcl,ipmaxexcluded,nombredchp,ipgateway,mascara,red):
        module = "Cisco-IOS-XE-native:native/ip/dhcp"
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"   
        payload =  {
            "Cisco-IOS-XE-native:dhcp": {
                "Cisco-IOS-XE-dhcp:excluded-address": {
                    "low-high-address-list": 
                    [
                        {
                            "low-address": ipminexcl,
                            "high-address": ipmaxexcluded
                        }
                    ]
                },
                "Cisco-IOS-XE-dhcp:pool": [
                    {
                        "id": nombredchp,
                        "default-router": {
                            "default-router-list": 
                            [
                                ipgateway
                            ]
                        },
                        "dns-server": 
                        {
                            "dns-server-list": 
                            [
                                "8.8.8.8"
                            ]
                        },
                        "network": {
                            "primary-network": 
                            {
                                "number": red,
                                "mask": mascara
                             }
                         }
                     }
                 ] 
             }    
        }
        self.Peticiones_patch(url,payload)
#Crear SNMP
    def Snmp(self,comunidad,tipo):
        if (tipo == 'Lectura'):
             permiso='ro'
             opcion = 'RO'
        else:
             permiso= 'rw'
             opcion = 'RW'
        print(tipo)
        my_json = r'null'
        my_dict = json.loads(my_json)
        my_json_again = json.dumps(my_dict)
        print(my_json_again) 

        module = 'Cisco-IOS-XE-native:native/snmp-server'
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"    
        payload = {
            "Cisco-IOS-XE-native:snmp-server": {
                "Cisco-IOS-XE-snmp:community": [
                    {
                        "name": comunidad,
                        "access-list-name": permiso
                    }
                ]
            }
            
        }
        print(payload)
        self.Peticiones_patch(url,payload)

# Metodo show
# 1 Mostrar nombre
# 2 Ver las interfaces con su IP
# 3 Ver todas las tablas ARP
# 4 Ver protocolos de capa 3
# 5 ver los host 
# 6 ver usuarios
# 7 ver tablas de enrutamiento
# 8 estadisticas del trafico del router
# 9 reporte de los vecinos cercanos
# 10 ver los procesos activos
# 11 Ver las estadisticas de memoria
# 12 mostrar vlans
    def Opciones_show(self,opcion):
        match opcion:
            case 1:
                module ="Cisco-IOS-XE-native:native/hostname"
            case 2:
                module ="Cisco-IOS-XE-native:native/ip/dhcp" 
            case 3:
                module = "ietf-interfaces:interfaces/interface"
            case 4:
                module = "Cisco-IOS-XE-native:native" 
            case 5:
                module = 'Cisco-IOS-XE-native:native/username'
            case 6:
                module = "Cisco-IOS-XE-native:native/interface/Vlan"
            case 7:
                module = 'Cisco-IOS-XE-native:native/router=router-ospf'
            case 8:
                module = 'Cisco-IOS-XE-memory-oper:memory-statistics'
            case 9:
                module = 'Cisco-IOS-XE-process-cpu-oper:cpu-usage'
            case 10:
                module = 'system'
            case 11:
                module = 'Cisco-IOS-XE-native:native/snmp-server'
            case 12:
                mensaje = 'vlan-membership'
            case _:
                mensaje = 'Error'
        
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"
        payload={
             "Cisco-IOS-XE-native": {
                 "show":"hola"
             }
        }
        respuesta_json=self.Peticiones_get(url,payload)
        respuesta_string=str(respuesta_json)
        return respuesta_string
       
# Metodo para resolver peticiones del tipo put 
    def Peticiones_put(self,url,payload):
        requests.packages.urllib3.disable_warnings()
        response = requests.put(url, headers=self.headers, data=json.dumps(payload), auth=(self.Usuario, self.Contrasenia), verify=False)       
        if (response.status_code == 204 or response.status_code == 201):
            print("Successfully updated interface")
        else:
            print("Issue with updating interface")

#Metodo para resolver peticiones del tipo get
    def Peticiones_get(self,url,payload):
        requests.packages.urllib3.disable_warnings()
        respuesta = requests.get(url, headers=self.headers, data=json.dumps(payload), auth=(self.Usuario, self.Contrasenia), verify=False)
        respuesta_json=respuesta.json()
        return respuesta_json
#Metodo para resolver peticiones del tipo patch
    def Peticiones_patch(self,url,payload):
        requests.packages.urllib3.disable_warnings()
        respuesta = requests.patch(url, headers=self.headers, data=json.dumps(payload), auth=(self.Usuario, self.Contrasenia), verify=False)
        if (respuesta.status_code == 204 or respuesta.status_code == 201):
            print("Successfully updated interface")
        else:
            print("Issue with updating interface")


#Pruebas de funcionamiento
#showvla = Servicio('admin','cisco12345','10.10.10.1')
#showvla.Configuracion_DHCP("30.30.30.1","30.30.30.10","Rest","30.30.30.1","255.255.255.0","30.30.30.0")
#respuestag=showvla.Opciones_show(2)
#print(respuestag)
#respuestag=showvla.Opciones_show(4)
#resultados=str(respuestag)

    
#df=pd.DataFrame.from_dict(respuestag)
#print(df)
