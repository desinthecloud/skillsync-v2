# SkillSync v2 — Clean Start
Minimal, reliable AWS app.
- Frontend: HTML/JS/CSS on S3 + CloudFront
- Backend: SAM (HTTP API + Lambda/Python + DynamoDB)
- CI/CD: GitHub Actions via OIDC

## Quick Start
1) `./scripts/deploy_backend.sh` → copy API URL
2) `export SITE_BUCKET="skillsync-yourunique"` then `./scripts/deploy_frontend_infra.sh`
3) Set `frontend/config.js` → `window.API_BASE_URL = "<your api>"` and re-run step 2 if needed.

## API
- GET `/health`
- GET `/skills?userId=...`
- POST `/skills` → `{ userId, name, level?, notes? }`
- PUT `/skills/{id}` → include `userId` and updated fields
- DELETE `/skills/{id}?userId=...`

## Cleanup
- `sam delete --stack-name skillsync-backend`
- `./scripts/cleanup.sh`
