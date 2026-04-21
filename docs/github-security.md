# GitHub Security Guidance

## Recommended Repository Settings

### Secret Protection
- Enable secret scanning.
- Enable push protection for secrets.
- Restrict repository secrets to required environments only.
- Add a clear security contact and a private reporting path.
- Review secret scanning alerts before each release.

### Branch Protection
Require these rules on the default branch:
- Pull request reviews before merge.
- At least one approval for normal changes.
- Required status checks for backend tests and frontend build.
- Dismiss stale approvals when code changes.
- Require linear history.
- Restrict direct pushes.
- Restrict force pushes.
- Require conversation resolution before merge.
- Require signed commits if the repository policy supports it.

### Deployment Controls
- Use environment-specific secrets in GitHub Actions.
- Deploy only from protected branches.
- Use separate GitHub environments for staging and production.
- Approve production deploys manually if the deployment platform supports it.
- Rotate secrets on a defined schedule.
- Remove unused repository secrets and environment secrets.

### CI Expectations
- Backend tests must pass.
- Frontend production build must pass.
- Dependency updates must be reviewed.
- No build artifacts, SQLite files, or local env files should be committed.

## Operational Notes
- Keep `.env` files out of the repository.
- Keep local database files out of version control.
- Store service credentials in the deployment platform secret store.
- Use short-lived tokens where possible.
- Rotate API keys and signing secrets on a schedule.
- Review `docs/release-checklist.md` before each release.
