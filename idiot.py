import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('YOUR_APIKEY')

base_url = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"

headers = {
    "Content-Type": "application/json"
}

params = {
    "jsonrpc": "2.0",
    "method": "cmdb.objects.read",
    "params": {
			"categories":  ["C__CATG__CPU"],
      "apikey": api_key,
      "language": "en"
    },
	    "id": 1
}


response = requests.post(base_url, headers= headers, data=json.dumps(params), verify=False)
print((json.dumps(response.json(), indent = 4)))
