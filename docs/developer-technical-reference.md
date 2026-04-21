# Developer Technical Reference

This document maps source code modules to responsibilities and workflows.

## Backend Module Responsibilities

### app/main.py

- FastAPI bootstrap
- CORS setup
- startup backend verification (PostgreSQL + Redis)
- router registration

### app/config.py

- typed runtime configuration from environment
- includes database URL, redis URL, HMAC and rate limits

### app/database.py

- async SQLAlchemy engine and session factory
- Base metadata root

### app/models

- agent.py: agent identity + api key hash + status
- wallet.py: balance and currency (one wallet per agent)
- policy.py: strict policy controls and thresholds
- transaction.py: spend outcomes + idempotency key
- audit_log.py: event payload records for traceability

### app/schemas

- request and response validation contracts
- strict typed input for spend/policy/wallet endpoints

### app/dependencies.py

- API key authentication
- HMAC signature + timestamp validation
- replay key protection
- rate limiting and velocity checks
- Redis-backed request protection only

### app/services/policy_engine.py

Decision order:

1. per transaction limit
2. vendor allowlist
3. blocked category
4. daily total
5. monthly total
6. approval threshold

Return states:

- APPROVED
- REJECTED
- PENDING_APPROVAL

### app/services/spend_service.py

- idempotency check before new transaction create
- wallet and policy row locking
- policy evaluation and reason code propagation
- balance deduction on approved path only
- mock payment adapter call
- audit event generation

### app/services/payment_adapter.py

- replaceable interface point
- current mock implementation returns SUCCESS

### app/services/audit_service.py

- centralized audit log write helper

### app/routers

- agents.py: create/list agents
- wallet.py: fund/get wallet
- policy.py: set policy
- spend.py: signed spend endpoint
- transactions.py: list transactions
- audit_logs.py: list audit entries

## Frontend Module Responsibilities

### app/layout.tsx + components/Nav.tsx

- global shell and route navigation

### app/dashboard/page.tsx

- agent and wallet display
- transaction metrics and recent activity

### app/transactions/page.tsx

- transaction table with status/reason visibility

### app/policy-editor/page.tsx

- policy input form
- backend response JSON view

### app/alerts/page.tsx

- audit activity feed for governance visibility

### lib/api.ts

- centralized API fetch wrappers

## Security Flow Summary

Spend call security gate order:

1. X-API-Key auth
2. X-Timestamp freshness
3. X-Signature HMAC validation
4. replay key check
5. rate limit and velocity checks
6. strict policy evaluation and transactional spend handling

### Local Development Modes

- Production-only runtime expects PostgreSQL + Redis.
- Use the test suite for isolated SQLite coverage only.
