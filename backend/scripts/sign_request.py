import hashlib
import hmac
import json
import sys


# Usage:
# python scripts/sign_request.py POST /spend 2026-04-21T12:00:00Z '{"a":1}' 'your_api_key'


def main() -> None:
    if len(sys.argv) != 6:
        print("usage: sign_request.py METHOD PATH TIMESTAMP JSON_BODY API_KEY")
        raise SystemExit(1)

    method = sys.argv[1]
    path = sys.argv[2]
    timestamp = sys.argv[3]
    raw_body = sys.argv[4]
    api_key = sys.argv[5]

    body = json.dumps(json.loads(raw_body), separators=(",", ":"))
    canonical = f"{method}|{path}|{timestamp}|".encode("utf-8") + body.encode("utf-8")
    signature = hmac.new(api_key.encode("utf-8"), canonical, hashlib.sha256).hexdigest()

    print(signature)


if __name__ == "__main__":
    main()
