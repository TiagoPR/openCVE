from idoit import IDoit
from search_vendor import get_cves_with_versions 

def parse_version(version):
    """Convert a version string into a tuple of integers for comparison."""
    try:
        return tuple(map(int, version.split('.')))
    except ValueError:
        # Handle cases where version strings might not be valid integers
        return tuple(map(int, (version.split('.') + ['0', '0'])[:3]))

def is_version_affected(version, start_version, end_version):
    """Check if a version falls within the start and end version range."""
    parsed_version = parse_version(version)
    
    if start_version:
        parsed_start_version = parse_version(start_version)
        if parsed_version < parsed_start_version:
            return False
    
    if end_version:
        parsed_end_version = parse_version(end_version)
        if parsed_version > parsed_end_version:
            return False
    
    return True

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
                cves = get_cves_with_versions(os_title)
                if cves:
                    for cve, details in cves.items():
                        print("cve: ", cve)
                        print("details: ", details, "\n")
                        if is_version_affected(os_version, details.get('start_version'), details.get('end_version')):
                            print(f"Hey this {infrastructure} has a vulnerability on OS {os_title} version {os_version} due to {cve}\n")
        
        # Check applications
        for app in obj['applications']:
            app_title = app.get('title')
            app_version = app.get('version')
            if app_title and app_version:
                cves = get_cves_with_versions(app_title)
                if cves:
                    for cve, details in cves.items():
                        print("cve: ", cve)
                        print("details: ", details, "\n")
                        if is_version_affected(app_version, details.get('start_version'), details.get('end_version')):
                            print(f"Hey the {tipo} {infrastructure} has a vulnerability on software {app_title} version {app_version} due to {cve}\n")
