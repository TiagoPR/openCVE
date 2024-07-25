import requests
import json
import os
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

api_key = os.getenv('YOUR_APIKEY')

base_url = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"

headers = {
    "Content-Type": "application/json"
}

print("Do you want to add a APP or OS?")
value = input("1 - APP \n2- OS")

match value:
	case "1":
		title = input("Application name?")
		params = {
		    "method": "cmdb.object.create",
		    "params": {
		        "apikey": api_key,
		        "type": "C__OBJTYPE__APPLICATION",
		        "title": title,
		        "category": "C__CATG__APPLICATION"
		    },
		    "id": 1,
		    "jsonrpc": "2.0"
		}
		response = requests.post(base_url, headers= headers, data=json.dumps(params), verify=False)
		print((json.dumps(response.json(), indent = 4)))

		id = response.json()['result']['id']
		version = input("Which version?")
		params = {
			"version": "2.0",
			"method": "cmdb.category.save",
			"params": {
				"object": id,
			        "data": {
					"application": id,
					"assigned_version": version 
			        },
			        "category": "C__CATG__APPLICATION",
			        "apikey": api_key,
				"language": "en"
			    },
			    "id": 1
		}
		response = requests.post(base_url, headers= headers, data=json.dumps(params), verify=False)
		print((json.dumps(response.json(), indent = 4)))
	case "2":
		title = input("OS name?")
		params = {
		    "method": "cmdb.object.create",
		    "params": {
		        "apikey": api_key,
		        "type": "C__OBJTYPE__OPERATING_SYSTEM",
		        "title": title,
		        "category": "C__CATG__OPERATING_SYSTEM"
		    },
		    "id": 1,
		    "jsonrpc": "2.0"
		}
		response = requests.post(base_url, headers= headers, data=json.dumps(params), verify=False)
		print((json.dumps(response.json(), indent = 4)))

		id = response.json()['result']['id']
		version = input("Which version?")
		params = {
			"version": "2.0",
			"method": "cmdb.category.save",
			"params": {
				"object": id,
			        "data": {
					"application": id,
					"assigned_version": version 
			        },
			        "category": "C__CATG__OPERATING_SYSTEM",
			        "apikey": api_key,
				"language": "en"
			    },
			    "id": 1
		}
		response = requests.post(base_url, headers= headers, data=json.dumps(params), verify=False)
		print((json.dumps(response.json(), indent = 4)))
	case _:
		print("Wrong input")
		exit()
