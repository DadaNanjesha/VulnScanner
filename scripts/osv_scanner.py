import requests
import json

# Function to scan the package using the OSV API and check if it has vulnerabilities
def scan_dependencies_with_osv_api(dependencies):
    """Scan dependencies with OSV API for vulnerabilities."""

    # OSV URL for searching vulnerabilities of a specific package in PyPI
    osv_url = f"https://api.osv.dev/v1/query"

    # Construct the query, omitting the version field to search across all versions
    query = {
        "version": "",
        "package": {"name": dependencies["name"], "ecosystem": "PyPI"},
    }

    try:
        # Send a POST request to the OSV API
        response = requests.post(osv_url, json=query)

        if response.status_code == 200:
            result = response.json()

            if result.get("vulnerabilities"):
                print(f"Vulnerabilities found for {dependencies['name']}:")
                for vuln in result["vulnerabilities"]:
                    print(f"- {vuln['id']}: {vuln['summary']}")

                    # Check if vulnerability ID matches "MAL" (indicating it is malicious)
                    if "MAL" in vuln["id"]:
                        print(
                            f"  WARNING: This vulnerability is flagged as malicious: {vuln['summary']}"
                        )
            else:
                print(f"No vulnerabilities found for {dependencies['name']}, ")
                print(json.dumps(result, indent=2))

        else:
            print(f"Error querying OSV API: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error querying OSV API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from scan result: {e}")
        return None

# Example usage
dependencies = {
    "name": "requests",  # Example package name
}

# Scan the package with OSV and check for vulnerabilities
scan_results = scan_dependencies_with_osv_api(dependencies)

if scan_results:
    print("Scan Results:", json.dumps(scan_results, indent=4))
