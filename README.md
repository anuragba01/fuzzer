
# HTTP Parameter Fuzzer

A lightweight Python-based HTTP fuzzing tool for security testing, bug bounty reconnaissance, and parameter-based vulnerability discovery.
It loads a list of targets and payloads, automatically builds test requests, logs responses, and saves results in structured JSON.

---

## Features

* Automated HTTP requests with payload injection
* Support for multiple targets and parameters
* Customizable headers & rate limiting
* Detailed logging (status code, headers, body snippet)
* JSON output for easy analysis
* Graceful error handling
* Simple, readable implementation
* Works with any endpoint using query parameters

---

## How It Works

1. Load targets from `target.txt`
   Format:

   ```
   host_path,parameter
   ```

   Example:

   ```
   example.com/search,q
   example.com/item,id
   ```

2. Load payloads from `payload.txt`

   * One payload per line

3. Run the fuzzer

4. For each combination, the tool makes a request like:

   ```
   https://example.com/search?q=<payload>
   ```

5. Responses are logged into `fuzzing_results.json`

---

## Requirements

* Python 3.8+
* `requests` library

Install dependency:

```bash
pip install requests
```

---

## Usage

### 1. Add your targets

Create `target.txt`:

```
example.com/login,user
example.com/search,q
```

### 2. Add your payloads

Create `payload.txt`:

```
'
"
<>
test123
1 OR 1=1
```

### 3. Run the fuzzer

```bash
python fuzzer.py
```

### 4. Review results

Output file:

```
fuzzing_results.json
```

Each entry contains:

* URL tested
* Status code
* Headers
* Body snippet
* Error message (if any)

---

## Output Example

```json
{
    "timestamp": "2025-01-10T12:00:00Z",
    "request_url": "https://example.com/search?q=test",
    "base_host_path": "example.com/search",
    "parameter": "q",
    "payload": "test",
    "status_code": 200,
    "response_headers": { "Content-Type": "text/html" },
    "response_body_snippet": "<html>..."
}
```

---

## Configuration

Modify these constants inside `fuzzer.py`:

```python
RATE_LIMIT_DELAY = 0.1
REQUEST_TIMEOUT = 10
HEADERS = {'User-Agent': 'Bugcrowd-Fuzzer'}
```

---

## Project Structure

```
fuzzer.py
target.txt
payload.txt
fuzzing_results.json
README.md
```

---

## Disclaimer

This tool is for **legal security testing only**.
Do not use it on systems you do not own or have explicit permission to test.

---

## License

It is licensed under the MIT License.
