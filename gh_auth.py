import requests
import time
import sys

client_id = "178c6fc778ccc68e1d6a"
resp = requests.post("https://github.com/login/device/code", data={"client_id": client_id}, headers={"Accept": "application/json"}).json()

print(f"URL: {resp['verification_uri']}")
print(f"CODE: {resp['user_code']}")

with open("github_device_info.txt", "w") as f:
    f.write(f"{resp['device_code']}\n{resp['interval']}")
