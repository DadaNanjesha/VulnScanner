import requests
import json

# Function to scan the package using the OSV API and check if it has vulnerabilities
def scan_dependencies_with_osv_api(dependencies):
    """Scan dependencies with OSV API for vulnerabilities."""
    "https://osv.dev/list?q=requests&ecosystem=PyPI"
    package_name =dependencies.get("name")
    # OSV URL for searching vulnerabilities of a specific package in PyPI
    osv_url = f"https://osv.dev/list?q={package_name}&ecosystem=PyPI"
    
    try:
        # Send a GET request to the OSV search URL
        response = requests.get(osv_url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the response JSON
        result = response.json()

        # Check if vulnerabilities were found
        if 'vulnerabilities' in result and result['vulnerabilities']:
            print(f"Vulnerabilities found for {dependencies['name']} version {dependencies['version']}:")
            for vuln in result['vulnerabilities']:
                print(f"- {vuln.get('id', 'Unknown ID')}: {vuln.get('summary', 'No summary available')}")
                # Check for any flags indicating malicious activity (based on vulnerability descriptions)
                if "malicious" in vuln.get("summary", "").lower():
                    print(f"  WARNING: Malicious indicator found: {vuln.get('summary')}")
        else:
            print(f"No vulnerabilities found for {dependencies['name']} version {dependencies['version']}.")

        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error querying OSV API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from scan result: {e}")
        return None

# Example usage
dependencies = {
    "name": "requests",         # Example package name
    "version": "2.26.0"         # Example version
}

# Scan the package with OSV and check for vulnerabilities
scan_results = scan_dependencies_with_osv_api(dependencies)

if scan_results:
    print("Scan Results:", json.dumps(scan_results, indent=4))
