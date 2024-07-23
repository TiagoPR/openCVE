from read import readVersions
from search_vendor import fetch_cves_vendor
import json

versions = readVersions()
if versions:
	for title in versions:
		version = versions[title]
		cves = fetch_cves_vendor(title)
		cves_json = cves.json()
		if cves_json:
			print(json.dumps(cves_json, indent=4))

