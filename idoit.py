import argparse
import requests
import json
import io
import csv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constants
API_URL = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"
CONF_PATH = '.conf'

class IDoit:
    def __init__(self, config_path='.conf', url="https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php") -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.config_path = config_path
        self.url = url
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_api_key(self, tenant):
        with open(self.config_path, 'r') as file:
            for line in file:
                if line.startswith(tenant):
                    return line.split('=')[1].strip()
        raise ValueError(f"API key for environment '{tenant}' not found in .conf file.")

    def make_request(self, method, params, api_key):
        payload = {
            "version": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        params['apikey'] = api_key
        try:
            response = requests.post(self.url, json=payload, headers=self.headers, verify=False)
            response.raise_for_status()
            return response.json().get('result', [])
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []

    def get_all_objects(self, api_key):
        return self.make_request("cmdb.objects.read", {}, api_key)

    def get_objects_by_titles(self, objects, titles):
        return [obj for obj in objects if obj['title'] in titles]

    def get_category_info(self, api_key, obj_id, category):
        params = {
            "objID": obj_id,
            "category": category
        }
        return self.make_request("cmdb.category.read", params, api_key)

    def get_info(self, api_key, obj, info_type):
        category_map = {
            "OperatingSystem": "C__CATG__OPERATING_SYSTEM",
            "Application": "C__CATG__APPLICATION",
        }
        if info_type == "Support":
            return {"CMDB_Status": obj.get('cmdb_status_title', 'N/A')}
        elif info_type in category_map:
            category_info = self.get_category_info(api_key, obj['id'], category_map[info_type])
            if category_info:
                # Extract only the assigned_version field
                assigned_version = next((item.get('assigned_version') for item in category_info if 'assigned_version' in item), 'N/A')
                return {"assigned_version": assigned_version}
            else:
                return None
        else:
            return None

    def has_category(self, api_key, obj_id, category_constant):
        result = self.get_category_info(api_key, obj_id, category_constant)
        return len(result) > 0

    def filter_objects_by_categories(self, api_key, objects):
        return [obj for obj in objects if self.has_category(api_key, obj['id'], "C__CATG__APPLICATION") or 
                self.has_category(api_key, obj['id'], "C__CATG__OPERATING_SYSTEM")]

    def get_version_info(self, api_key, obj_id):
        category_constant = 'C__CATG__VERSION'
        result = self.get_category_info(api_key, obj_id, category_constant)
        if not result:
            print(f"No version data retrieved for objID {obj_id}")
            return None
        version_info = result[0]
        return version_info.get('title', 'Unknown Version')

    def fetch_hardware_objects(self, api_key):
        hardware_types = [
            'server',
            'switch',
            'router',
            'firewall',
            'storage system',
            'blade server',
            'enclosure',
            'pdu',
            'rack',
            'workstation',
            'net connector',
            'virtual server'
        ]
        
        # Convert all types to lowercase for case-insensitive matching
        hardware_types = [t.lower() for t in hardware_types]
        
        # Fetch all objects
        all_objects = self.get_all_objects(api_key)
        
        # Filter objects based on their type_title, case-insensitive
        hardware_objects = []
        for obj in all_objects:
            if obj['type_title'].lower() in hardware_types:
                hardware_objects.append({
                    'id': obj['id'],
                    'title': obj['title'],
                    'type': obj['type_title'],
                    'cmdb_status': obj['cmdb_status_title']
                })
        
        return hardware_objects

    def fetch_hardware_objects_with_details(self, api_key):
        hardware_objects = self.fetch_hardware_objects(api_key)
        
        enriched_objects = []
        for obj in hardware_objects:
            obj_id = obj['id']
            
            # Fetch operating system information
            os_info = self.get_category_info(api_key, obj_id, "C__CATG__OPERATING_SYSTEM")
            if os_info:
                obj['operating_system'] = {
                    'title': os_info[0].get('title', 'N/A'),
                    'version': os_info[0].get('version', 'N/A')
                }
            else:
                obj['operating_system'] = {'title': 'N/A', 'version': 'N/A'}
            
            # Fetch application information
            app_info = self.get_category_info(api_key, obj_id, "C__CATG__APPLICATION")
            if app_info:
                obj['applications'] = [
                    {
                        'title': app.get('title', 'N/A'),
                        'version': app.get('version', 'N/A')
                    } for app in app_info
                ]
            else:
                obj['applications'] = []
            
            enriched_objects.append(obj)
        
        return enriched_objects

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def dict_to_csv(data):
    if not data:
        return ""

    output = io.StringIO()
    writer = csv.writer(output)

    # Flatten and collect all unique keys
    all_keys = set()
    flattened_data = {}
    for title, obj in data.items():
        flat_obj = flatten_dict(obj)
        all_keys.update(flat_obj.keys())
        flattened_data[title] = flat_obj

    # Ensure 'Title' is the first column
    columns = ['Title'] + sorted(all_keys)

    # Write headers
    writer.writerow(columns)

    # Write data rows
    for title, flat_obj in flattened_data.items():
        row = [title] + [flat_obj.get(key, 'N/A') for key in columns[1:]]
        writer.writerow(row)

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description="i-doit CLI tool")
    parser.add_argument("-c", "--config", default=CONF_PATH, help="Your own configuration file")
    parser.add_argument("-u", "--url", default=API_URL, help="Url you wish")
    parser.add_argument("-t", "--tenant", required=True, help="The tenant you want to use (e.g., test)")
    parser.add_argument("-o", "--objects", required=True, nargs='+', help="List of objects to retrieve information from")
    parser.add_argument("-i", "--info", required=False, nargs='+', 
                        help="List of info types to retrieve (OperatingSystem, Application, Support)")
    parser.add_argument("-f", "--format", choices=['json', 'csv'], default='json', help="Output format (json or csv)")
    args = parser.parse_args()

    idoit = IDoit(args.config, args.url)

    try:
        api_key = idoit.get_api_key(args.tenant)
    except ValueError as e:
        print(e)
        return

    all_objects = idoit.get_all_objects(api_key)
    requested_objects = idoit.get_objects_by_titles(all_objects, args.objects)

    if not requested_objects:
        print("No requested objects found.")
        return

    results = {}
    for obj in requested_objects:
        obj_title = obj['title']
        results[obj_title] = {}

        if args.info:
            for info_type in args.info:
                info = idoit.get_info(api_key, obj, info_type)
                if info is not None:
                    results[obj_title][info_type] = info
                else:
                    results[obj_title][info_type] = f"No info available for {info_type}"

    if args.format == 'json':
        print(json.dumps(results, indent=4))
    elif args.format == 'csv':
        print(dict_to_csv(results))

if __name__ == "__main__":
    main()
