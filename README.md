# Wayback Extractor

A minimal command-line tool to pull archived URLs for a domain from the [Wayback Machine](https://web.archive.org) CDX API. Supports plain text, CSV, and JSON output, and can optionally route requests through a local Tor SOCKS5 proxy.

## Features

- 🔎 Queries the Wayback Machine's CDX/timemap API for a given domain
- 🌐 Includes subdomains by default (prefix match), or restrict to the exact domain
- 📄 Export results as `txt`, `csv`, or `json`
- 🧅 Optional routing through Tor (`-p` flag, expects a local Tor SOCKS5 proxy on `127.0.0.1:9050`)
- 🔁 Automatic retry with exponential backoff on HTTP 429 (rate limiting)

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/wayback-extractor.git
cd wayback-extractor
```

Install dependencies (only needed if you plan to use the `-p` Tor proxy option):

```bash
pip install -r requirements.txt
```

No external dependencies are required for normal (non-Tor) usage — the script only relies on the Python standard library in that case.

## Usage

```bash
python3 wayback_extractor.py <domain> [options]
```

### Options

| Flag | Description | Default |
|---|---|---|
| `domain` | Target domain (required) | — |
| `-f`, `--format` | Output format: `txt`, `csv`, or `json` | `txt` |
| `-o`, `--output` | Save output to a file instead of printing to stdout | — |
| `-l`, `--limit` | Maximum number of results to fetch | `10000` |
| `--no-subdomains` | Exclude subdomains, match the exact domain only | off |
| `-p` | Route requests through a local Tor SOCKS5 proxy (`127.0.0.1:9050`) | off |

### Examples

Fetch all archived URLs for a domain (plain text to stdout):

```bash
python3 wayback_extractor.py example.com
```

Save results as CSV, excluding subdomains:

```bash
python3 wayback_extractor.py example.com -f csv -o results.csv --no-subdomains
```

Export as JSON, limiting to 500 records:

```bash
python3 wayback_extractor.py example.com -f json -l 500 -o results.json
```

Route requests through Tor:

```bash
python3 wayback_extractor.py example.com -p
```

> **Note:** the `-p` option assumes Tor is already running locally and exposing a SOCKS5 proxy on port `9050` (the default for the Tor daemon / Tor Browser). It does not start Tor for you.

## Output fields

Each record returned by the CDX API includes:

- `original` — the archived URL
- `mimetype` — content type at capture time
- `timestamp` — first capture timestamp
- `endtimestamp` — most recent capture timestamp
- `groupcount` — number of captures grouped
- `uniqcount` — number of unique captures

## Requirements

- Python 3.7+
- [`PySocks`](https://pypi.org/project/PySocks/) (only required for the `-p` Tor option)

## Use cases

This tool is commonly used for reconnaissance during authorized security testing and OSINT research, such as discovering historical endpoints, forgotten subdomains, or old parameters that may still be relevant to an attack surface review. **Only use it against domains you own or are explicitly authorized to test.**

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Disclaimer

This tool queries publicly available data from the Wayback Machine. Use responsibly and in accordance with the target's terms of service and applicable law. The author(s) assume no liability for misuse.
