import os
from typing import Dict, Optional
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import re

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
    return response.json()

def fetch_cve_details(cve_id):
    """ Fetch details for a specific CVE. """
    url = f"{base_url}/{cve_id}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response.json()

def parse_version_from_configurations(configurations):
    """ Parse the version information from the configurations field. """
    for config in configurations:
        for node in config.get('nodes', []):
            for cpe_match in node.get('cpeMatch', []):
                start_version = cpe_match.get('versionStartIncluding')
                end_version = cpe_match.get('versionEndExcluding')
                if start_version or end_version:
                    return {
                        'start_version': start_version,
                        'end_version': end_version
                    }
    return None

def get_cves_with_versions(vendor):
    """ Get CVEs with their versions for a specific vendor. """
    cves = fetch_cves_vendor(vendor)
    cve_dict = {}

    # Handle the case where cves is a list
    if isinstance(cves, list):
        cve_list = cves
    else:
        # If it's not a list, assume it's a dict with a 'results' key
        cve_list = cves.get('results', [])

    for cve in cve_list:
        cve_id = cve['id']
        cve_details = fetch_cve_details(cve_id)
        details = cve_details.get('raw_nvd_data', [])
        configurations = details.get('configurations', [])
        version_info = parse_version_from_configurations(configurations)
        
        if version_info:
            cve_dict[cve_id] = version_info

    return cve_dict

#def fetch_cves_search(vendor):
#    """ Fetch CVEs from the API for a specific keyword. """
#    params = {'search': vendor}
#    response = requests.get(base_url, auth=HTTPBasicAuth(username, password), params=params)
#    return response
#
#def vendor_vulnerabilities(vendor):
#    response = fetch_cves_vendor(vendor)
#    if response.status_code != 200:
#        print(f"Failed to retrieve CVEs for {vendor}: {response.status_code}")
#        return
#    
#    cve_list = response.json()
#    
#    dic = {}
#    for cve in cve_list:
#        cve_id = cve.get('id')
#        if cve_id:
#            cve_url = f'http://127.0.0.1:8000/api/cve/{cve_id}'
#    
#            cve_response = requests.get(cve_url, auth=HTTPBasicAuth(username, password))
#    
#            if cve_response.status_code == 200:
#                #print(f"Success! Fetched details for CVE: {cve_id}")
#                cve_details = cve_response.json()
#                #print(json.dumps(cve_details, indent=4))
#    
#                configurations = cve_details['raw_nvd_data'].get('configurations', [])
#                for config in configurations:
#                    nodes = config.get('nodes', [])
#                    for node in nodes:
#                        cpe_matches = node.get('cpeMatch', [])
#                        for match in cpe_matches:
#                            if match.get('vulnerable', False):
#                                criteria = match.get('criteria')
#                                software = criteria.split(':')[4]
#                                version = criteria.split(':')[5]
#                                # Check if software key exists in dictionary, if not, initialize set
#                                if software not in dic:
#                                    dic[software] = set()
#                                # Add version to the set for the corresponding software
#                                dic[software].add(version)
#    return dic
#
#def search_vulnerabilities(vendor):
#    response = fetch_cves_search(vendor)
#    if response.status_code != 200:
#        print(f"Failed to retrieve CVEs: {response.status_code}")
#        exit()
#    
#    cve_list = response.json()
#    
#    for cve in cve_list:
#        cve_id = cve.get('id')
#        if cve_id:
#            cve_url = f'http://127.0.0.1:8000/api/cve/{cve_id}'
#    
#            cve_response = requests.get(cve_url, auth=HTTPBasicAuth(username, password))
#    
#            if cve_response.status_code == 200:
#                print(f"Success! Fetched details for CVE: {cve_id}")
#                cve_details = cve_response.json()
#                if not cve_details['raw_nvd_data'].get('configurations'):
#                    print(json.dumps(cve_details, indent=4))

def main():

    vendor = input("Which vendor do you want to search for? ")
    vulnerabilities = get_cves_with_versions(vendor)
    print(vulnerabilities)
    #search_vulnerabilities(vendor)

if __name__ == "__main__":
    main()
