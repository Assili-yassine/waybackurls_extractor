# Wayback Extractor

A minimal command-line tool to pull archived URLs for a domain from the [Wayback Machine](https://web.archive.org) CDX API. Supports plain text, CSV, and JSON output, and can optionally route requests through a local Tor SOCKS5 proxy.

## Features

- 🔎 Queries the Wayback Machine's CDX/timemap API for a given domain
- 🌐 Includes subdomains by default (prefix match), or restricts to the exact domain
- 📄 Export results as `txt`, `csv`, or `json`
- 🧅 Optional routing through Tor (`-p` flag, expects a local Tor SOCKS5 proxy on `127.0.0.1:9050`)
- 🔁 Automatic retry with exponential backoff on HTTP 429 (rate limiting)
- ⚡ Install once and run from anywhere as `wayback`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Assili-yassine/wayback-extractor.git
cd wayback-extractor
```

Install dependencies (only needed if you plan to use the `-p` Tor proxy option):

```bash
pip install -r requirements.txt
```

### Install as a system command (recommended)

Rename the script, make it executable, and move it into your system PATH:

```bash
mv wayback_extractor.py wayback
chmod +x wayback
sudo mv wayback /usr/local/bin/
```

Now you can run it from anywhere:

```bash
wayback example.com
```

> **Note:** If you modify the script later, simply replace the copy in `/usr/local/bin/` with the updated version.

---

## Usage

```bash
wayback <domain> [options]
```

If you prefer not to install it system-wide, you can also run it directly:

```bash
python3 wayback_extractor.py <domain> [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `domain` | Target domain (required) | — |
| `-f`, `--format` | Output format: `txt`, `csv`, or `json` | `txt` |
| `-o`, `--output` | Save output to a file instead of printing to stdout | — |
| `-l`, `--limit` | Maximum number of results to fetch | `10000` |
| `--no-subdomains` | Exclude subdomains, match the exact domain only | disabled |
| `-p` | Route requests through a local Tor SOCKS5 proxy (`127.0.0.1:9050`) | disabled |

---

## Examples

Fetch all archived URLs:

```bash
wayback example.com
```

Save results as CSV, excluding subdomains:

```bash
wayback example.com -f csv -o results.csv --no-subdomains
```

Export as JSON with a maximum of 500 records:

```bash
wayback example.com -f json -l 500 -o results.json
```

Route requests through Tor:

```bash
wayback example.com -p
```

If running without installation:

```bash
python3 wayback_extractor.py example.com
```

> **Note:** The `-p` option assumes Tor is already running locally and exposing a SOCKS5 proxy on `127.0.0.1:9050`. The tool does not start Tor automatically.

---

## Output Fields

Each record returned by the CDX API includes:

| Field | Description |
|-------|-------------|
| `original` | Archived URL |
| `mimetype` | Content type at capture time |
| `timestamp` | First capture timestamp |
| `endtimestamp` | Most recent capture timestamp |
| `groupcount` | Number of grouped captures |
| `uniqcount` | Number of unique captures |

---

## Requirements

- Python 3.7+
- `PySocks` *(only required when using the `-p` option)*

---

## Use Cases

Wayback Extractor is useful during authorized security testing and OSINT research for:

- Finding historical endpoints
- Discovering forgotten files
- Recovering old API paths
- Identifying deprecated parameters
- Enumerating archived subdomains

**Only use this tool against domains you own or are explicitly authorized to test.**

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool queries publicly available data from the Internet Archive's Wayback Machine. Users are responsible for ensuring their use complies with applicable laws, regulations, and the target organization's policies. The author assumes no liability for misuse.
