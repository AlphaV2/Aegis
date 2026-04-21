import hashlib
import hmac
import json
from datetime import datetime, timezone

import httpx


BASE = "http://127.0.0.1:8000"
API_KEY = ""


def sign(method: str, path: str, timestamp: str, body: str) -> str:
    canonical = f"{method}|{path}|{timestamp}|".encode("utf-8") + body.encode("utf-8")
    return hmac.new(API_KEY.encode("utf-8"), canonical, hashlib.sha256).hexdigest()


def post_spend(client: httpx.Client, payload: dict):
    path = "/spend"
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    body = json.dumps(payload, separators=(",", ":"))
    sig = sign("POST", path, ts, body)
    return client.post(
        BASE + path,
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
            "X-Timestamp": ts,
            "X-Signature": sig,
        },
        timeout=20,
    )


def main() -> None:
    global API_KEY
    with httpx.Client() as client:
        health = client.get(BASE + "/health", timeout=10)
        print("health", health.status_code, health.text)

        create = client.post(BASE + "/agents", json={"name": "e2e-agent"}, timeout=10)
        create.raise_for_status()
        created = create.json()
        agent_id = created["agent"]["id"]
        API_KEY = created["api_key"]

        fund = client.post(
            BASE + "/wallet/fund",
            json={"agent_id": agent_id, "amount": "5000.00"},
            timeout=10,
        )
        fund.raise_for_status()

        policy = client.post(
            BASE + "/policy/set",
            json={
                "agent_id": agent_id,
                "per_tx_limit": "1000.00",
                "daily_limit": "3000.00",
                "monthly_limit": "15000.00",
                "allowed_vendors": ["openai", "aws", "supabase"],
                "blocked_categories": ["gambling", "adult"],
                "requires_approval_above": "700.00",
            },
            timeout=10,
        )
        policy.raise_for_status()

        approved_payload = {
            "agent_id": agent_id,
            "amount": "120.00",
            "vendor": "openai",
            "category": "infra",
            "idempotency_key": "idem_demo_approved_1",
        }
        rejected_payload = {
            "agent_id": agent_id,
            "amount": "50.00",
            "vendor": "unknown_vendor",
            "category": "infra",
            "idempotency_key": "idem_demo_reject_1",
        }
        pending_payload = {
            "agent_id": agent_id,
            "amount": "900.00",
            "vendor": "openai",
            "category": "infra",
            "idempotency_key": "idem_demo_pending_1",
        }

        r1 = post_spend(client, approved_payload)
        print("approved", r1.status_code, r1.text)

        r2 = post_spend(client, rejected_payload)
        print("rejected", r2.status_code, r2.text)

        r3 = post_spend(client, pending_payload)
        print("pending", r3.status_code, r3.text)

        r4 = post_spend(client, approved_payload)
        print("duplicate", r4.status_code, r4.text)

        tx = client.get(BASE + "/transactions", timeout=10)
        logs = client.get(BASE + "/audit-logs", timeout=10)
        print("transactions_count", len(tx.json()))
        print("audit_logs_count", len(logs.json()))


if __name__ == "__main__":
    main()
