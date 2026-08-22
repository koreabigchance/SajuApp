import requests
import time
import subprocess
import sys
import os

client_id = "178c6fc778ccc68e1d6a"
with open("github_device_info.txt", "r") as f:
    device_code, interval = f.read().splitlines()

interval = int(interval)

for i in range(120): # poll for ~10 minutes
    time.sleep(interval)
    resp = requests.post("https://github.com/login/oauth/access_token", data={"client_id": client_id, "device_code": device_code, "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}, headers={"Accept": "application/json"}).json()
    if 'access_token' in resp:
        token = resp['access_token']
        
        # Authenticate gh CLI
        process = subprocess.Popen(['C:\\Program Files\\GitHub CLI\\gh.exe', 'auth', 'login', '--with-token'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = process.communicate(input=token)
        
        # Configure Git user
        subprocess.run([os.path.expandvars('%USERPROFILE%\\MinGit\\cmd\\git.exe'), 'config', '--global', 'user.name', 'SajuApp Developer'], check=False)
        subprocess.run([os.path.expandvars('%USERPROFILE%\\MinGit\\cmd\\git.exe'), 'config', '--global', 'user.email', 'developer@sajuapp.com'], check=False)
        
        print("SUCCESS")
        sys.exit(0)
    elif resp.get('error') != 'authorization_pending':
        print(f"FAILED: {resp}")
        sys.exit(1)

print("TIMEOUT")
sys.exit(1)
