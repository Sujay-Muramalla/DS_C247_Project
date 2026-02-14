#!/usr/bin/env python3
"""
Semi-automated TI lookup helper (offline-friendly scaffolding).

- abuse.ch URLhaus: query URL/domain
- abuse.ch MalwareBazaar: query SHA-256
- VirusTotal: optional (requires VT_API_KEY)

NOTE: Requires internet access from your runtime environment.
"""

import os, sys, json, time
import requests

VT_API_KEY = os.getenv("VT_API_KEY")

def urlhaus_lookup(url_or_domain: str):
    endpoint = "https://urlhaus-api.abuse.ch/v1/url/"
    r = requests.post(endpoint, data={"url": url_or_domain}, timeout=30)
    return r.json()

def malwarebazaar_lookup_sha256(sha256: str):
    endpoint = "https://mb-api.abuse.ch/api/v1/"
    r = requests.post(endpoint, data={"query":"get_info","hash":sha256}, timeout=30)
    return r.json()

def virustotal_lookup_hash(sha256: str):
    if not VT_API_KEY:
        raise RuntimeError("VT_API_KEY not set. Export VT_API_KEY in your shell.")
    endpoint = f"https://www.virustotal.com/api/v3/files/{sha256}"
    headers = {"x-apikey": VT_API_KEY}
    r = requests.get(endpoint, headers=headers, timeout=30)
    return r.json()

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python ti_lookup.py urlhaus <url_or_domain>")
        print("  python ti_lookup.py malwarebazaar <sha256>")
        print("  python ti_lookup.py vt <sha256>   (requires VT_API_KEY)")
        sys.exit(1)

    mode = sys.argv[1].lower()
    q = sys.argv[2].strip()

    if mode == "urlhaus":
        out = urlhaus_lookup(q)
    elif mode == "malwarebazaar":
        out = malwarebazaar_lookup_sha256(q)
    elif mode == "vt":
        out = virustotal_lookup_hash(q)
    else:
        raise SystemExit("Unknown mode: " + mode)

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
