from dotenv import load_dotenv
from idoit import IDoit
#import certifi
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

IDOIT_API_URL = 'https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php'
CONF_PATH = ".conf" 
TENANT = "test"

def readVersions(idoit, api_key):
    # Get all objects
    objects = idoit.get_all_objects(api_key)
    
    if not objects:
        print("No objects retrieved or failed to retrieve objects.")
        return {}
    
    # Filter objects by categories
    filtered_objects = idoit.filter_objects_by_categories(api_key, objects)
    
    if not filtered_objects:
        print("No objects matched the categories.")
        return {}
    
    # Get versions for filtered objects
    versions = {}
    for obj in filtered_objects:
        obj_id = obj['id']
        obj_title = obj['title']
        version_title = idoit.get_version_info(api_key, obj_id)
        versions[obj_title] = version_title
    
    return versions

def main():
    idoit = IDoit(CONF_PATH, IDOIT_API_URL)
    api_key = idoit.get_api_key(TENANT)
    
    versions = readVersions(idoit, api_key)
    if versions:
        for title, version_title in versions.items():
            print(f"Title: {title}, Version: {version_title}")
    else:
        print("No objects or versions found")

if __name__ == "__main__":
    main()
