import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime

load_dotenv()

username = os.getenv('YOUR_USERNAME')
password = os.getenv('YOUR_PASSWORD')

if not username or not password:
    raise ValueError("Username or password environment variables not set")

base_url = 'http://127.0.0.1:8000/api/cve'

today = datetime.now().date()

def fetch_cves(page):
    """ Fetch CVEs from the API for a specific page. """
    params = {'page': page}
    response = requests.get(base_url, auth=HTTPBasicAuth(username, password), params=params)
    return response

def cves_updated_today(cve_list):
    """ Filter CVEs that are updated today. """
    updated_today = []
    for cve in cve_list:
        updated_at = cve.get('updated_at')
        if updated_at:
            update_date = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ').date()
            if update_date == today:
                updated_today.append(cve)
            else:
                return updated_today, False  
    return updated_today, True

all_updated_cves = []
page = 1
while True:
    response = fetch_cves(page)
    if response.status_code != 200:
        print(f"Failed to retrieve CVEs: {response.status_code}")
        break

    cve_list = response.json()
    if not cve_list:
        break  

    updated_cves, all_today = cves_updated_today(cve_list)
    all_updated_cves.extend(updated_cves)

    if not all_today:
        break 

    page += 1 

for cve in all_updated_cves:
    cve_id = cve.get('id')
    if cve_id:
        cve_url = f'http://127.0.0.1:8000/api/cve/{cve_id}'
        
        cve_response = requests.get(cve_url, auth=HTTPBasicAuth(username, password))

        if cve_response.status_code == 200:
            print(f"Success! Fetched details for CVE: {cve_id}")
            cve_details = cve_response.json()
            
            print(json.dumps(cve_details, indent=4))
        else:
            print(f"Failed to retrieve details for CVE: {cve_id} - Status Code: {cve_response.status_code}")
