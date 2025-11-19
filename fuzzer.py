import csv
import requests
import json
import os
import time
from datetime import datetime

# --- Configuration ---
TARGET_FILE = "target.txt"
PAYLOAD_FILE = "payload.txt"
OUTPUT_JSON = "fuzzing_results.json"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
REQUEST_TIMEOUT = 10
RATE_LIMIT_DELAY = 0.1  # 100ms between requests
# ---------------------

class Fuzzer:
    def __init__(self, target_file, payload_file):
        self.targets = self._load_file(target_file)
        self.payloads = self._load_file(payload_file)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.all_results = []
        self.request_counter = 0

    def _load_file(self, filepath):
        """Loads lines from a file, stripping whitespace."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Error: Required file not found at '{filepath}'")
        with open(filepath, 'r') as f:
            # Assuming targets are in format: host_path,parameter
            return [line.strip() for line in f if line.strip()]

    def run(self):
        """Runs the entire fuzzing process."""
        print(f"Loaded {len(self.payloads)} payloads and {len(self.targets)} targets.")
        
        for row in self.targets:
            try:
                # Expects target file to be CSV-like: example.com/path,param_name
                host_path, parameter = row.split(',', 1)
            except ValueError:
                print(f"Skipping malformed target row: '{row}'. Expected format: 'host_path,parameter'")
                continue

            for payload in self.payloads:
                self.request_counter += 1
                url = f"https://{host_path}?{parameter}={payload}"
                print(f"[{self.request_counter}] Testing URL: {url}")
                
                result = self._run_single_test(url, host_path, parameter, payload)
                self.all_results.append(result)

                time.sleep(RATE_LIMIT_DELAY)

    def _run_single_test(self, url, host_path, parameter, payload):
        """Executes and logs a test for a single URL."""
        result_log = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_url': url,
            'base_host_path': host_path,
            'parameter': parameter,
            'payload': payload,
            'status_code': None,
            'response_headers': None,
            'response_body_snippet': None,
            'error': None
        }

        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            result_log.update({
                'status_code': response.status_code,
                'response_headers': dict(response.headers),
                'response_body_snippet': response.text[:20000] # Log a snippet of the body
            })

        except requests.exceptions.RequestException as e:
            print(f"  -> Request failed: {e}")
            result_log['error'] = str(e)
        
        return result_log

    def save_results(self, output_file):
        """Saves all collected results to a JSON file."""
        print(f"\nFuzzing complete. Total requests made: {self.request_counter}")
        with open(output_file, 'w') as f:
            json.dump(self.all_results, f, indent=4)
        print(f"All results saved to '{output_file}'")

def main():
    """Main function to initialize and run the fuzzer."""
    try:
        fuzzer = Fuzzer(TARGET_FILE, PAYLOAD_FILE)
        fuzzer.run()
        fuzzer.save_results(OUTPUT_JSON)
    except FileNotFoundError as e:
        print(e)
        return

if __name__ == "__main__":
    main()
