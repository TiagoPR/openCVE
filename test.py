import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"

try:
    response = requests.get(url, verify=False)
    print(f"Connection successful. Status code: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
