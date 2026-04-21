# Security Policy

## Reporting Security Issues

If you discover a vulnerability in Aegis Layer, do not open a public issue with exploit details.

Report it privately to the repository maintainers through the platform's security advisory workflow or the team's internal security contact.

## Safe Handling Rules
- Do not commit secrets, API keys, private certificates, or access tokens.
- Do not commit local `.env` files.
- Do not commit generated databases, build artifacts, or dependency directories.
- Review dependency updates before merging.
- Require pull request review for production changes.
