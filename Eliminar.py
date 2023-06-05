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

module = "ietf-interfaces:interfaces"

url = f"https://{device['ip']}:{device['port']}/restconf/data/{module}/interface=Loopback10000"
print(url)

requests.packages.urllib3.disable_warnings()
response = requests.delete(url, headers=headers, auth=(device['username'], device['password']), verify=False)

print(response)

if (response.status_code == 204):
   print("Successfully deleted interface")
else:
   print("Issue with deleting interface")