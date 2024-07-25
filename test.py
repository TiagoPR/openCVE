import requests

url = "https://idoit.svc.eurotux.pt/i-doit/src/jsonrpc.php"
cert_path = "certs/root.pem"  # Update this path

try:
    response = requests.get(url, verify=cert_path)
    print(f"Connection successful. Status code: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
