import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

username = os.getenv('YOUR_USERNAME')
password = os.getenv('YOUR_PASSWORD')

if not username or not password:
    raise ValueError("Username or password environment variables not set")

base_url = 'http://127.0.0.1:8000/api/cve'

def fetch_cves_vendor(vendor):
    """ Fetch CVEs from the API for a specific vendor. """
    params = {'vendor': vendor}
    response = requests.get(base_url, auth=HTTPBasicAuth(username, password), params=params)
    return response

def fetch_cves_search(vendor):
    """ Fetch CVEs from the API for a specific keyword. """
    params = {'search': vendor}
    response = requests.get(base_url, auth=HTTPBasicAuth(username, password), params=params)
    return response

def vendor_vulnerabilities(vendor):
    response = fetch_cves_vendor(vendor)
    if response.status_code != 200:
        print(f"Failed to retrieve CVEs: {response.status_code}")
        exit()
    
    cve_list = response.json()
    
    for cve in cve_list:
        cve_id = cve.get('id')
        if cve_id:
            cve_url = f'http://127.0.0.1:8000/api/cve/{cve_id}'
    
            cve_response = requests.get(cve_url, auth=HTTPBasicAuth(username, password))
    
            if cve_response.status_code == 200:
                print(f"Success! Fetched details for CVE: {cve_id}")
                cve_details = cve_response.json()
                #print(json.dumps(cve_details, indent=4))
    
                configurations = cve_details['raw_nvd_data'].get('configurations', [])
                dic = {}
                for config in configurations:
                    nodes = config.get('nodes', [])
                    for node in nodes:
                        cpe_matches = node.get('cpeMatch', [])
                        for match in cpe_matches:
                            if match.get('vulnerable', False):
                                criteria = match.get('criteria')
                                software = criteria.split(':')[4]
                                version = criteria.split(':')[5]
                                # Check if software key exists in dictionary, if not, initialize set
                                if software not in dic:
                                    dic[software] = set()
                                # Add version to the set for the corresponding software
                                dic[software].add(version)
                for software, versions in dic.items():
                    for version in versions:
                        print(f"Vendor: {vendor}, Software: {software}, Version: {version} is vulnerable.")
                return dic

def search_vulnerabilities(vendor):
    response = fetch_cves_search(vendor)
    if response.status_code != 200:
        print(f"Failed to retrieve CVEs: {response.status_code}")
        exit()
    
    cve_list = response.json()
    
    for cve in cve_list:
        cve_id = cve.get('id')
        if cve_id:
            cve_url = f'http://127.0.0.1:8000/api/cve/{cve_id}'
    
            cve_response = requests.get(cve_url, auth=HTTPBasicAuth(username, password))
    
            if cve_response.status_code == 200:
                print(f"Success! Fetched details for CVE: {cve_id}")
                cve_details = cve_response.json()
                if not cve_details['raw_nvd_data'].get('configurations'):
                    print(json.dumps(cve_details, indent=4))

def main():

    vendor = input("Which vendor do you want to search for? ")
    vendor_vulnerabilities(vendor)
    search_vulnerabilities(vendor)

if __name__ == "__main__":
    main()
