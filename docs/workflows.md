# Workflows

## Spend Orchestration Workflow
1. Request enters POST /spend.
2. API key is validated against agent hash.
3. Rate-limit and velocity checks run in Redis.
4. Signature and timestamp are validated.
5. Replay cache key is checked and set.
6. Row-level lock is acquired for wallet and policy (SELECT FOR UPDATE).
7. Idempotency uniqueness is checked.
8. Policy engine evaluates all strict rules.
9. Decision branch:
   - APPROVED: balance check, deduction, mock adapter charge, persist transaction.
   - REJECTED: persist rejection reason.
   - PENDING_APPROVAL: persist pending state.
10. Audit log entries are written for each critical stage.
11. DB commit finalizes all writes atomically.

## Policy Evaluation Order
1. Per transaction limit.
2. Vendor allowlist.
3. Blocked category.
4. Daily aggregate limit.
5. Monthly aggregate limit.
6. Approval threshold.

## Idempotency Workflow
1. Spend request uses idempotency_key.
2. Existing transaction with same (agent_id, idempotency_key):
   - If payload matches key intent, return existing transaction result.
   - If payload differs, return 409 conflict.
3. New key persists one transaction and one deterministic outcome.

## Replay Attack Defense Workflow
1. Signature key uses agent API key.
2. Canonical signed payload is method|path|timestamp|body.
3. Freshness window uses max age seconds from settings.
4. Redis replay key rejects repeated signatures inside freshness window.

## Partial Failure Safety
1. Wallet deduction and transaction insert happen in one DB transaction.
2. Adapter failure raises HTTP error before commit.
3. DB rollback preserves previous wallet balance and state consistency.
