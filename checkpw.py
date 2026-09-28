#!/usr/bin/env python3
"""Check if a password has appeared in a breach (Have I Been Pwned, k-anonymity)."""

import argparse
import hashlib
import sys

try:
    import requests
except ImportError:
    sys.exit("Error: requests is not installed. Run: pip install -r requirements.txt")

HIBP_URL = "https://api.pwnedpasswords.com/range/{}"
USER_AGENT = "passwordscan-cli/1.0"


def check_password(password: str) -> int:
    """Return how many times the password appeared in breaches."""
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]

    r = requests.get(
        HIBP_URL.format(prefix),
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    r.raise_for_status()

    for line in r.text.splitlines():
        tail, count = line.split(":")
        if tail == suffix:
            return int(count)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check if a password has been breached (Have I Been Pwned)."
    )
    parser.add_argument(
        "password",
        nargs="?",
        help="Password to check (if omitted, read from secure prompt)",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File with one password per line",
    )
    args = parser.parse_args()

    passwords: list[str] = []
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            passwords = [ln.strip() for ln in fh if ln.strip()]
    elif args.password:
        passwords = [args.password]
    else:
        import getpass

        password = getpass.getpass("Password: ")
        if password:
            passwords = [password]

    if not passwords:
        sys.exit("No password provided.")

    failed = False
    for password in passwords:
        try:
            count = check_password(password)
        except Exception as exc:
            failed = True
            print(f"[ERROR] {exc}", file=sys.stderr)
            continue
        if count:
            print(f"Breached {count} times")
        else:
            print("Not breached (0 times)")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
