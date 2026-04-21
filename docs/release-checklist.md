# GitHub Release Checklist

Use this checklist before every production or staging release.

## Repository Security
- Secret scanning is enabled.
- Push protection is enabled.
- Dependabot alerts are enabled.
- Dependabot updates are enabled for `pip` and `npm`.
- No `.env`, `.sqlite`, `.db`, `node_modules`, or `.next` artifacts are committed.

## Branch Protection
- Require pull request reviews before merge.
- Require at least one approval.
- Require backend tests and frontend build checks.
- Require linear history.
- Restrict direct pushes to the protected branch.
- Restrict force pushes.
- Dismiss stale approvals after code changes.

## Deployment Controls
- Use protected branches only.
- Use environment-specific secrets for staging and production.
- Keep API keys and signing secrets in GitHub Secrets or the deployment platform secret store.
- Deploy only after CI succeeds.
- Use manual approval for production deployments if supported.

## Release Validation
- Backend tests pass.
- Frontend build passes.
- Security headers and CSP remain intact.
- Postgres and Redis configuration is present for runtime.
- Audit logging still records spend, rejection, and approval events.

## Commit Strategy
- Keep commits small and focused.
- Use separate commits for backend, frontend, and docs changes.
- Use descriptive messages that describe the user-facing scope.