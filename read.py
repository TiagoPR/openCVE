import requests
import os
from dotenv import load_dotenv

load_dotenv()

IDOIT_API_URL = 'https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php'
API_KEY = os.getenv('YOUR_APIKEY')

def get_all_objects():
    payload = {
        "version": "2.0",
        "method": "cmdb.objects.read",
        "params": {
            "apikey": API_KEY
        },
        "id": 1
    }
    try:
        response = requests.post(IDOIT_API_URL, json=payload, verify=False)
        response.raise_for_status()
        #print(response.json())
        return response.json().get('result', [])
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def has_category(obj_id, category_constant):
    payload = {
        "version": "2.0",
        "method": "cmdb.category.read",
        "params": {
            "apikey": API_KEY,
            "objID": obj_id,
            "category": category_constant,
            "language": "en"
        },
        "id": 1
    }
    try:
        response = requests.post(IDOIT_API_URL, json=payload, verify=False)
        response.raise_for_status()
        #print(response.json())
        result = response.json().get('result', [])
        print(f"Category check for objID {obj_id} and category {category_constant}: {result}")
        return len(result) > 0
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def filter_objects_by_categories(objects):
    filtered_objects = []
    for obj in objects:
        obj_id = obj['id']
        if has_category(obj_id, "C__CATG__APPLICATION") or has_category(obj_id, "C__CATG__OPERATING_SYSTEM"):
            filtered_objects.append(obj)
    return filtered_objects

def get_version_info(obj_id):
    category_constant = 'C__CATG__VERSION'

    payload = {
        "version": "2.0",
        "method": "cmdb.category.read",
        "params": {
            "apikey": API_KEY,
            "objID": obj_id,
            "category": category_constant,
            "language": "en"
        },
        "id": 1
    }
    try:
        response = requests.post(IDOIT_API_URL, json=payload, verify=False)
        response.raise_for_status()
        #print(response.json())
        result = response.json().get('result', [])
        if not result:
            print(f"No version data retrieved for objID {obj_id}")
            return None
        version_info = result[0]
        return version_info.get('title', 'Unknown Version')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def readVersions():
    # Get all objects
    objects = get_all_objects()
    
    if not objects:
        print("No objects retrieved or failed to retrieve objects.")
        exit()
    
    # Filter objects by categories
    filtered_objects = filter_objects_by_categories(objects)
    
    if not filtered_objects:
        print("No objects matched the categories.")
    else:
        # Print filtered objects with version
        versions = {}
        for obj in filtered_objects:
            obj_id = obj['id']
            obj_title = obj['title']
            version_title = get_version_info(obj_id)
            versions[obj_title] = version_title
        return versions 

def main():
    versions = readVersions()
    if versions:
        for title in versions:
            version_title = versions[title]
            print(f"Title: {title}, Version: {version_title}")
    else:
        print("No objects or versions found")

if __name__ == "__main__":
    main()
