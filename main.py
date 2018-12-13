import requests
import json

r = requests.get("https://api.stratz.com/api/v1/Hero")
r_json=json.loads(r.text)
r_len = len(r_json)
for key, value in r_json.items():
    print("id: " + str(r_json[key]['id']))
print("SUCCESS")
