# API Examples

## 1) Create Agent
POST /agents

Request body
{
  "name": "ops-agent"
}

Response (sample)
{
  "agent": {
    "id": "c4f8f1ee-0d14-47fd-9cc8-fa22f0f19311",
    "name": "ops-agent",
    "status": "ACTIVE"
  },
  "api_key": "ag_xxx"
}

## 2) Fund Wallet
POST /wallet/fund

Request body
{
  "agent_id": "c4f8f1ee-0d14-47fd-9cc8-fa22f0f19311",
  "amount": "2000.00"
}

## 3) Set Policy
POST /policy/set

Request body
{
  "agent_id": "c4f8f1ee-0d14-47fd-9cc8-fa22f0f19311",
  "per_tx_limit": "600.00",
  "daily_limit": "1800.00",
  "monthly_limit": "8000.00",
  "allowed_vendors": ["openai", "aws"],
  "blocked_categories": ["gambling", "adult"],
  "requires_approval_above": "450.00"
}

## 4) Spend (Signed)
POST /spend
Headers
X-API-Key: ag_xxx
X-Timestamp: 2026-04-21T12:00:00Z
X-Signature: <computed_hmac>

Request body
{
  "agent_id": "c4f8f1ee-0d14-47fd-9cc8-fa22f0f19311",
  "amount": "120.00",
  "vendor": "openai",
  "category": "infra",
  "idempotency_key": "idem_0001"
}

Possible status values
APPROVED
REJECTED
PENDING_APPROVAL

## 5) Read Transactions
GET /transactions

## 6) Read Audit Logs
GET /audit-logs
