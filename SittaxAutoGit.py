import requests
import subprocess
import os

def get_latest_release_exe_link(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    response = requests.get(url)
    
    if response.status_code == 200:
        releases = response.json()
        if releases:
            latest_release = max(releases, key=lambda r: r['created_at'])
            
            tag_name = latest_release.get('tag_name')
            created_at = latest_release.get('created_at')
            assets = latest_release.get('assets', [])
            
            exe_asset = next((asset for asset in assets if asset['name'].endswith('.exe') and not asset['name'].endswith('.blockmap')), None)
            
            if exe_asset:
                exe_url = exe_asset['browser_download_url']
                print(f"Latest Version: {tag_name}")
                print(f"Date: {created_at}")
                print(f"Exe Download Link: {exe_url}")
                
                exe_filename = exe_url.split('/')[-1]
                
                if os.path.exists(exe_filename):
                    print(f"Removing existing file: {exe_filename}")
                    os.remove(exe_filename)
                
                comando = ["wget", exe_url]
                resultado = subprocess.run(comando, capture_output=True, text=True)
                
                print("Saída do comando:", resultado.stdout)
                print("Erros (se houver):", resultado.stderr)
            else:
                print("No .exe file found in the latest release.")
        else:
            print("No releases found.")
    else:
        print("Failed to fetch releases")
        print(f"Status code: {response.status_code}")

get_latest_release_exe_link('DevEderNO', 'nf-monitor')
