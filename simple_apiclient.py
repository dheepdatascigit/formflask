# simple api script to test the API locally

import requests
import json

url = "http://127.0.0.1:5000/api"

payload = '{"vlanid": 5, "subnet": "203.0.1.0/24", "desc": "main interface WAN"}'
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
print()

[print(x) for x in json.loads(response.text.encode('utf8'))["genconfig"]]

