# Aegis Layer Architecture

## Core Path
Agent -> API Gateway (FastAPI route + dependencies) -> Policy Engine -> Decision
Decision APPROVED -> Wallet Deduction -> Payment Adapter (mock)
Decision REJECTED -> Log + Alert feed visibility
Decision PENDING_APPROVAL -> Pending state + log

## Backend Modules
- routers: endpoint layer, dependency wiring, HTTP contract.
- services: business logic and orchestration.
- models: SQLAlchemy ORM persistence schema.
- schemas: Pydantic validation and responses.
- utils: security and helper primitives.

## Data Stores
- PostgreSQL: source of truth for agents, wallets, policies, transactions, audit logs.
- Redis: rate limiting, velocity counters, replay cache.

## Security Controls
- Per-agent API key authentication.
- HMAC request signing.
- Timestamp freshness validation.
- Replay detection cache.
- Idempotency keys with DB unique constraint.
- Row-lock transaction safety to prevent concurrent double spending.

## Decision Model
- APPROVED: strict policy pass and sufficient balance.
- REJECTED: any hard policy violation or insufficient balance.
- PENDING_APPROVAL: amount above approval threshold.
