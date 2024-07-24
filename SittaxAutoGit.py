import requests
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
                
                script_content = f"#!/bin/bash\n\nwget {exe_url}\n"
                script_filename = "download_exe.sh"
                
                with open(script_filename, 'w') as script_file:
                    script_file.write(script_content)
                
                print(f"Script '{script_filename}' created successfully.")
            else:
                print("No .exe file found in the latest release.")
        else:
            print("No releases found.")
    else:
        print("Failed to fetch releases")
        print(f"Status code: {response.status_code}")

get_latest_release_exe_link('DevEderNO', 'nf-monitor')