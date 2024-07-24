import argparse
import requests
import json

# Constants
API_URL = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"
CONF_PATH = '.conf'

def get_api_key(tenant):
    with open(CONF_PATH, 'r') as file:
        for line in file:
            if line.startswith(tenant):
                return line.split('=')[1].strip()
    raise ValueError(f"API key for environment '{tenant}' not found in .conf file.")

def get_all_objects(api_key):
    payload = {
        "version": "2.0",
        "method": "cmdb.objects.read",
        "params": {
            "apikey": api_key 
        },
        "id": 1
    }
    try:
        response = requests.post(API_URL, json=payload, verify= False)
        response.raise_for_status()
        return response.json().get('result', [])
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def get_object(objetos, args):
    for objeto in objetos:
        if objeto['title'] == args.object:
            if args.info:
                obj_id = objeto['id']
                return obj_id
            print(json.dumps(objeto, indent=4))
            exit()

def get_info(api_key, id, args):
    match args.info:
        case "OperatingSystem":
            payload = {
                "version": "2.0",
                "method": "cmdb.category.read",
                "params": {
				    "objID": id,
				    "category": "C__CATG__OPERATING_SYSTEM",
                    "apikey": api_key 
                },
                "id": 1
            }
            try:
                response = requests.post(API_URL, json=payload, verify= False)
                response.raise_for_status()
                return response.json().get('result', [])
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return []
        case "Application":
            payload = {
                "version": "2.0",
                "method": "cmdb.category.read",
                "params": {
			"objID": id,
			"category": "C__CATG__APPLICATION",
                    "apikey": api_key 
                },
                "id": 1
            }
            try:
                response = requests.post(API_URL, json=payload, verify= False)
                response.raise_for_status()
                return response.json().get('result', [])
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return []
        case "Support":
            payload = {
                "version": "2.0",
                "method": "cmdb.category.read",
                "params": {
			"objID": id,
			"category": "C__CATG__SERVICE",
                    "apikey": api_key 
                },
                "id": 1
            }
            try:
                response = requests.post(API_URL, json=payload, verify= False)
                response.raise_for_status()
                return response.json().get('result', [])
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return []
        case _:
            print("There's no info about that")
            exit()


def main():
    parser = argparse.ArgumentParser(description="i-doit CLI tool")
    parser.add_argument("-t", "--tenant", required=True, help="The tenant you want to use (e.g., test)")
    parser.add_argument("-o", "--object", required=True, help="Which object you are going to want the information from")
    parser.add_argument("-i", "--info", required=False, help="Which info you want to see?\n -OperatingSystem\n -Application\n -Support\n")
    args = parser.parse_args()

    try:
        api_key = get_api_key(args.tenant)
    except ValueError as e:
        print(e)
        return

    objects = get_all_objects(api_key)

    obj_id = get_object(objects, args)

    info = get_info(api_key, obj_id, args)

    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    main()
