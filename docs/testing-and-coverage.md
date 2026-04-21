# Automated Testing and Coverage Notes

Date: 2026-04-21

## Test Framework

- pytest
- pytest-asyncio

Config:

- backend/pytest.ini
- asyncio mode: auto
- fixture loop scope: function

## Test Suite Implemented

Location:

- backend/tests/conftest.py
- backend/tests/test_policy_engine.py
- backend/tests/test_spend_idempotency.py

### Fixture Layer (conftest.py)

- Uses isolated in-memory SQLite database per test session fixture.
- Creates schema from SQLAlchemy metadata.
- Seeds one active agent + wallet + strict policy.
- Ensures deterministic values for policy thresholds and vendor allowlists.

### Policy Engine Coverage (test_policy_engine.py)

1. vendor_not_allowed rejection
2. amount_requires_approval pending decision
3. policy_passed approval decision

### Spend/Idempotency Coverage (test_spend_idempotency.py)

1. Duplicate request with same idempotency key returns same transaction
2. Same idempotency key with changed payload raises HTTP 409 conflict
3. Insufficient balance path sets REJECTED + insufficient_balance reason

## Test Run Output

Command:

- python -m pytest -q

Result:

- 6 passed

## Why This Coverage Matters

- Protects core objective correctness: APPROVED/REJECTED/PENDING behavior.
- Protects anti-double-spend behavior via idempotency semantics.
- Protects safety around wallet deduction boundaries.

## Recommended Next Coverage Expansion

1. API-level tests for /spend signature and replay headers.
2. Concurrent spend tests for row-lock behavior.
3. Rate-limit and velocity threshold tests (Redis live integration).
4. Golden tests for audit-log payload structure per event type.
