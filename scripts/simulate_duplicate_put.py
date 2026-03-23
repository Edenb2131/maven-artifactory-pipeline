#!/usr/bin/env python3
"""
simulate_duplicate_put.py

Deterministically reproduces the Artifactory 403 that the customer sees
when Maven 3.9.12 sends two concurrent PUT requests for the same artifact
to a user who has Deploy but NOT Delete/Overwrite permission.

What it does:
  1. Generates a unique artifact path for this run (so each execution starts fresh).
  2. PUT #1  →  uploads the artifact.  Expects 201 (Accepted Deploy).
  3. PUT #2  →  uploads to the SAME path again.  Expects 403 (Denied Delete)
               because the file now exists and overwriting requires Delete permission.

This mirrors exactly what Artifactory's access log shows in the customer's case:
  [ACCEPTED DEPLOY] ...javadoc.jar   ← PUT #1
  [DENIED DELETE]   ...javadoc.jar   ← PUT #2 (same file, milliseconds later)

Environment variables required:
  ARTIFACTORY_URL       Base URL, e.g. https://elinaf.jfrog.io/artifactory
  ARTIFACTORY_REPO      Target snapshot repository, e.g. edenb-pipeline-libs-snapshot
  DEPLOY_ONLY_USERNAME  User with Deploy but NOT Delete permission
  DEPLOY_ONLY_PASSWORD  Password for the above user
"""

import os
import sys
import ssl
import datetime
import urllib.request
import urllib.error
import base64

# Skip SSL verification for local runs (macOS Python 3.14 doesn't trust the
# JFrog Cloud cert chain by default). The GitHub Actions runner is unaffected.
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


def put_request(url: str, payload: bytes, username: str, password: str) -> tuple[str, int, str]:
    """Send a PUT request and return (iso_timestamp, status_code, response_body)."""
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(payload)),
        "User-Agent": "simulate_duplicate_put/1.0",
    }
    req = urllib.request.Request(url, data=payload, method="PUT", headers=headers)

    sent_at = datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds")
    try:
        with urllib.request.urlopen(req, context=_SSL_CTX) as resp:
            return sent_at, resp.status, resp.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return sent_at, e.code, e.read().decode(errors="replace")


def print_request(label: str, method: str, url: str, headers: dict, payload: bytes) -> None:
    print(f"  {method} {url}")
    for k, v in headers.items():
        display = "***" if k.lower() == "authorization" else v
        print(f"  {k}: {display}")
    print(f"  Body: <binary payload, {len(payload)} bytes>")


def main() -> None:
    base_url  = os.environ.get("ARTIFACTORY_URL",      "https://elinaf.jfrog.io/artifactory")
    repo      = os.environ.get("ARTIFACTORY_REPO",     "edenb-pipeline-libs-snapshot")
    username  = os.environ.get("DEPLOY_ONLY_USERNAME", "deploy-only-test")
    password  = os.environ.get("DEPLOY_ONLY_PASSWORD", "Password1!")

    # Unique path per run — ensures PUT #1 always hits a clean slot.
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S")
    artifact_path = (
        f"io/jfrog/example/duplicate-put-test/{ts}/"
        f"test-artifact-{ts}.bin"
    )
    url = f"{base_url}/{repo}/{artifact_path}"

    # Small payload that simulates a binary artifact (e.g. a javadoc jar).
    payload = b"SIMULATED_ARTIFACT_" + ts.encode() + b"\x00" * 512

    print("=" * 68)
    print("  Simulate Maven Duplicate PUT  →  Artifactory 403 Reproduction")
    print("=" * 68)
    print(f"\n  Artifactory URL : {base_url}")
    print(f"  Repository      : {repo}")
    print(f"  Deploy user     : {username}")
    print(f"  Artifact path   : {artifact_path}\n")

    request_headers = {
        "Authorization": f"Basic <redacted>",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(payload)),
        "User-Agent": "simulate_duplicate_put/1.0",
    }

    # ── PUT #1 ──────────────────────────────────────────────────────────────
    print("► PUT #1  (first upload — simulates Maven uploading the javadoc jar)")
    print()
    print_request("PUT #1", "PUT", url, request_headers, payload)
    print()
    sent1, status1, body1 = put_request(url, payload, username, password)
    print(f"  Timestamp : {sent1}")
    print(f"  HTTP      : {status1}")

    if status1 == 201:
        print("  ✓ ACCEPTED DEPLOY — file written to Artifactory\n")
    else:
        print(f"  ✗ Unexpected response: {body1[:300]}")
        sys.exit(1)

    # ── PUT #2 ──────────────────────────────────────────────────────────────
    print("► PUT #2  (duplicate upload — simulates Maven 3.9.12 second concurrent PUT)")
    print()
    print_request("PUT #2", "PUT", url, request_headers, payload)
    print()
    sent2, status2, body2 = put_request(url, payload, username, password)
    print(f"  Timestamp : {sent2}")
    print(f"  HTTP      : {status2}")

    if status2 == 403:
        print("  ✓ DENIED DELETE — overwrite blocked (user lacks Delete permission)")
        print(f"\n  Artifactory response: {body2.strip()[:400]}\n")
    elif status2 == 201:
        print("  Both uploads succeeded — deploy-only-test may have Delete permission.")
        print("  Remove Delete/Overwrite from the user's permission target and retry.\n")
    else:
        print(f"  Unexpected response: {body2[:400]}\n")

    # ── Summary ─────────────────────────────────────────────────────────────
    print("=" * 68)
    print("  Summary")
    print("=" * 68)
    print(f"  PUT #1  →  [{sent1}]  HTTP {status1}  (initial upload)")
    print(f"  PUT #2  →  [{sent2}]  HTTP {status2}  (same path, overwrite attempted)\n")

    if status1 == 201 and status2 == 403:
        print("  ✓ Reproduction successful.\n")
        print("  This is the exact sequence Artifactory logs in the customer's case:")
        print("    [ACCEPTED DEPLOY] ...javadoc.jar   ← PUT #1")
        print("    [DENIED DELETE]   ...javadoc.jar   ← PUT #2\n")
        print("  Root cause: Artifactory's overwrite operation requires Delete")
        print("  permission. When Maven 3.9.12 (resolver 1.9.25) fires two")
        print("  concurrent PUTs and the first completes before the second")
        print("  starts, the second PUT triggers an overwrite — which is blocked")
        print("  for a user with Deploy-only permission.")
        print()
        print(f"  Artifact left in repo for inspection:")
        print(f"    {url}")
        sys.exit(0)
    else:
        print("  ✗ Did not reproduce expected 201 → 403 sequence.")
        sys.exit(1)


if __name__ == "__main__":
    main()
