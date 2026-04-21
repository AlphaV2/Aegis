# Frontend Runtime and UI Verification

Date: 2026-04-21

## Runtime Launch

Backend launch command:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Frontend launch command:

```bash
cd frontend
npm run dev
```

Observed server startup:

- Next.js 15.0.4 started on http://localhost:3000
- FastAPI started on http://127.0.0.1:8000

## Route-Level Verification (Screenshot-Level Content Validation)

Pages opened and validated:

1. /dashboard
2. /transactions
3. /policy-editor
4. /alerts

Validated visible content in rendered output:

### Dashboard (/dashboard)

- Heading: Dashboard
- Cards visible: Transactions, Volume, Rejected
- Agents and wallets section visible
- Recent activity list visible with statuses APPROVED, REJECTED, PENDING_APPROVAL

### Transactions (/transactions)

- Heading: Transactions
- Table rows rendered with:
  - Time
  - Agent
  - Vendor
  - Amount
  - Status
  - Reason
- Statuses verified in table: APPROVED, REJECTED, PENDING_APPROVAL

### Policy Editor (/policy-editor)

- Heading: Policy Editor
- Form fields rendered:
  - agent_id
  - per_tx_limit
  - daily_limit
  - monthly_limit
  - allowed_vendors
  - blocked_categories
  - requires_approval_above
- JSON view panel visible

### Alerts (/alerts)

- Heading: Alerts and Activity
- Activity cards rendered with event types and payload JSON
- Verified event examples:
  - SPEND_ATTEMPT
  - SPEND_REJECTED
  - SPEND_PENDING
  - PAYMENT_SUCCESS
  - AGENT_CREATED
  - WALLET_FUNDED
  - POLICY_SET

## Verification Notes

- Route navigation shell rendered correctly across all pages.
- Theme direction verified in runtime:
  - dark background/surface
  - accent links/buttons
  - fintech-style low-clutter cards and tables
- UI data is live from backend endpoints, not static placeholders.
