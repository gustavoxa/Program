import requests
import json
from pprint import pprint


device = {
   "ip": "10.10.10.1",
   "username": "admin",
   "password": "cisco12345",
   "port": "443",
}

headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json", 
   }

module = "Cisco-IOS-XE-native:native/interface"

url = f"https://{device['ip']}:{device['port']}/restconf/data/{module}"
print(url)

requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=headers, auth=(device['username'], device['password']), verify=False).json()
#pprint(response)
interfaces = response['Cisco-IOS-XE-native:interface']['GigabitEthernet']
print(interfaces)
for interface in response:
   print(interface)