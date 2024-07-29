from read import readVersions
from idoit import IDoit
from search_vendor import vendor_vulnerabilities 

idoit = IDoit()
api_key = idoit.get_api_key('test')
versions = readVersions(idoit,api_key)
if versions:
	for title in versions:
		version = versions[title]
		cves = vendor_vulnerabilities(title)
		if cves:
			vulnerabilities = cves.get(title.lower())
			if vulnerabilities and version in vulnerabilities:
				print("FOUND A VULNERABILITY ON ", title, " VERSION ", version)

