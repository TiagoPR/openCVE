from idoit import IDoit
from search_vendor import vendor_vulnerabilities 

idoit = IDoit()
api_key = idoit.get_api_key('test')
objects = idoit.fetch_hardware_objects_with_details(api_key)

if objects:
    for obj in objects:
        infrastructure = obj['title']
        tipo = obj['type']
        
        # Check operating system
        os = obj['operating_system']
        if os and isinstance(os, dict):
            os_title = os.get('title')
            os_version = os.get('version')
            if os_title and os_version:
                cves = vendor_vulnerabilities(os_title)
                if cves:
                    vulnerabilities = cves.get(os_title.lower())
                    if vulnerabilities and os_version in vulnerabilities:
                        print(f"Hey this {infrastructure} has a vulnerability on OS {os_title} version {os_version}")
        
        # Check applications
        for app in obj['applications']:
            app_title = app.get('title')
            app_version = app.get('version')
            if app_title and app_version:
                cves = vendor_vulnerabilities(app_title)
                if cves:
                    vulnerabilities = cves.get(app_title.lower())
                    if vulnerabilities and app_version in vulnerabilities:
                        print(f"Hey the {tipo} {infrastructure} has a vulnerability on software {app_title} version {app_version}")
