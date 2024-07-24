from read import readVersions
from search_vendor import vendor_vulnerabilities 

versions = readVersions()
if versions:
	for title in versions:
		version = versions[title]
		cves = vendor_vulnerabilities(title)
		if cves:
			vulnerabilities = cves.get(title.lower())
			if vulnerabilities and version in vulnerabilities:
				print("FOUND A VULNERABILITY ON ", title, " VERSION ", version)

