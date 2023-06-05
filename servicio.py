import requests
import json
from pprint import pprint

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
        return url
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
    
# Cambiar nombre 
    def Nombre_dispositivo(self,nombre):
         module = "Cisco-IOS-XE-native:native/hostname"
         url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"        
         payload = {
             "hostname":
                    nombre
         }
         self.Peticiones_put(url,payload)
# Metodo show
# 1 Ver todas las interfaces
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
        module ="Cisco-IOS-XE-native:native"
        url = f"https://{self.Ip}:{self.port}/restconf/data/{module}"
        match opcion:
            case 1:
                mensaje = 'interfaces '
            case 2:
                mensaje = "ip interface brief"
            case 3:
                mensaje = "arp"
            case 4:
                mensaje = 'protocols' 
            case 5:
                mensaje = 'hosts'
            case 6:
                mensaje = 'users'
            case 7:
                mensaje = 'ip route summary'
            case 8:
                mensaje = 'ip traffic'
            case 9:
                mensaje = 'cdp neighbors detail'
            case 10:
                mensaje = 'processes'
            case 11:
                mensaje = 'memory'
            case 12:
                mensaje = 'vlan-membership'
            case _:
                mensaje = 'Error'
        payload={
             "Cisco-IOS-XE-native": {
                 "show": mensaje
             }
        }
        self.Peticiones_get(url,payload)        
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
        return respuesta
#Pruebas de funcionamiento
vlan = Servicio('admin','cisco12345','10.10.10.1')
print(vlan.Vlan_interface('Vlan700','20.80.60.2','255.255.255.0'))