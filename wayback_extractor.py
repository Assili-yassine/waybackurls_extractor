#!/usr/bin/env python3
# Minimal Wayback extractor with optional Tor SOCKS5 proxy (-p)

import argparse
import csv
import json
import sys
import io
import time
import urllib.request
import urllib.parse
import urllib.error

try:
    import socks
except ImportError:
    socks = None

CDX_API = "https://web.archive.org/web/timemap/json"
DEFAULT_FIELDS = "original,mimetype,timestamp,endtimestamp,groupcount,uniqcount"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://web.archive.org/",
}

MAX_RETRIES = 4
RETRY_DELAY = 10


def build_opener(proxy=None):
    handlers = []

    if proxy:
        if proxy.startswith("socks5://"):
            if socks is None:
                print("[-] PySocks is required for SOCKS5 support.")
                print("    pip install pysocks")
                sys.exit(1)

            import socket

            host, port = proxy.replace("socks5://", "").rsplit(":", 1)

            socks.set_default_proxy(
                socks.SOCKS5,
                host,
                int(port)
            )

            socket.socket = socks.socksocket

        else:
            handlers.append(
                urllib.request.ProxyHandler({
                    "http": proxy,
                    "https": proxy
                })
            )

    opener = urllib.request.build_opener(*handlers)
    opener.addheaders = list(HEADERS.items())
    return opener


def fetch_wayback(domain, limit=10000, subdomains=True, proxy=None):
    params = {
        "url": f"https://{domain}",
        "matchType": "prefix" if subdomains else "domain",
        "collapse": "urlkey",
        "output": "json",
        "fl": DEFAULT_FIELDS,
        "filter": "!statuscode:[45]..",
        "limit": str(limit),
    }

    url = CDX_API + "?" + urllib.parse.urlencode(params)

    opener = build_opener(proxy)
    req = urllib.request.Request(url)

    delay = RETRY_DELAY

    for attempt in range(MAX_RETRIES):
        try:
            with opener.open(req, timeout=90) as response:
                raw = response.read().decode()
            break

        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                print(f"[*] Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise

    data = json.loads(raw)

    if len(data) < 2:
        return []

    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]


def fmt_txt(records):
    return "\n".join(record["original"] for record in records)


def fmt_csv(records):
    if not records:
        return ""

    s = io.StringIO()
    writer = csv.DictWriter(s, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
    return s.getvalue()


def fmt_json(records):
    return json.dumps(records, indent=2)


FORMATS = {
    "txt": fmt_txt,
    "csv": fmt_csv,
    "json": fmt_json,
}


def clean(domain):
    return (
        domain.replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
    )


def main():
    parser = argparse.ArgumentParser(
        description="Minimal Wayback Machine URL Extractor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "domain",
        help="Target domain"
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=FORMATS,
        default="txt",
        help="Output format"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Save output to file"
    )

    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10000,
        help="Maximum number of results"
    )

    parser.add_argument(
        "--no-subdomains",
        action="store_true",
        help="Exclude subdomains"
    )

    parser.add_argument(
        "-p",
        action="store_true",
        help="Use Tor SOCKS5 proxy (127.0.0.1:9050)"
    )

    args = parser.parse_args()

    proxy = None

    if args.p:
        proxy = "socks5://127.0.0.1:9050"
        print("[+] Using Tor SOCKS5 proxy: socks5://127.0.0.1:9050")

    records = fetch_wayback(
        clean(args.domain),
        limit=args.limit,
        subdomains=not args.no_subdomains,
        proxy=proxy,
    )

    output = FORMATS[args.format](records)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"[+] Saved {len(records)} records to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
