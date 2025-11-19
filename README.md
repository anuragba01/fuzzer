
# HTTP Parameter Fuzzer

A lightweight Python-based HTTP parameter fuzzing tool for security testing, bug bounty reconnaissance, and parameter-based vulnerability discovery.
It loads a list of targets and payloads, automatically builds test requests, logs responses, and saves results in structured JSON.

---

## Features

* Automated HTTP requests with parameter fuzzing
* Customizable headers & rate limiting
* JSON output for easy analysis
* Graceful error handling
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

* Python 3.9+
* `requests` library

Install dependency:

```bash
pip install requests
```

---

## Usage
### 0.clone the repo 

    git clone https://github.com/anuragba01/fuzzer
    cd fuzzer

### 1. Add your targets

Create `target.txt`:

```
example.com/login,user
example.com/search,q
```

### 2. Add your payloads

Create `payload.txt`:

```
https://www.google.com,
http://www.example.com
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

## Disclaimer

This tool is for **legal security testing only**.
Do not use it on systems you do not own or have explicit permission to test.

---

## License

It is licensed under the MIT License.
