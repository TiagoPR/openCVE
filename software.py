from dotenv import load_dotenv
from idoit import IDoit
import urllib3
import json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

IDOIT_API_URL = 'https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php'
CONF_PATH = ".conf" 
TENANT = "test"

def main():
    idoit = IDoit(CONF_PATH, IDOIT_API_URL)
    api_key = idoit.get_api_key(TENANT)
    
    objects = idoit.fetch_hardware_objects_with_details(api_key)
    if objects:
        print(json.dumps(objects, indent=4))
    else:
        print("No objects or versions found")

if __name__ == "__main__":
    main()
