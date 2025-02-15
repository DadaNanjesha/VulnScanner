import subprocess
import json
import os

def scan_dependencies_with_osv_cli(lockfile_path, output_path):
    """Use OSV-Scanner CLI to scan dependencies and save the result in a JSON file."""
    # Check if the lockfile exists
    if not os.path.exists(lockfile_path):
        print(f"Error: The file '{lockfile_path}' does not exist.")
        return None

    # Construct the OSV-Scanner CLI command
    command = [
        "osv-scanner", "scan", 
        "--format", "json", 
        "-L", lockfile_path, 
        ">", output_path
    ]

    try:
        # Run the OSV-Scanner command via subprocess
        subprocess.run(" ".join(command), shell=True, check=True)
        print(f"OSV Scan completed. Results saved to '{output_path}'")

        # Load the results from the output JSON file
        with open(output_path, 'r') as f:
            result = json.load(f)

        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running OSV-Scanner CLI: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from scan result: {e}")
        return None

# Example usage
lockfile_path = r"data/Pipfile.lock"  # Use raw string to handle backslashes in paths
output_path = r"data/output.json"     # Use raw string to handle backslashes in paths
scan_results = scan_dependencies_with_osv_cli(lockfile_path, output_path)

if scan_results:
    print("OSV Scan Results:")
    print(scan_results)
