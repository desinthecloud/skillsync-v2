#!/usr/bin/env bash
set -euo pipefail
REGION="${AWS_REGION:-us-east-1}"; STACK_NAME="${STACK_NAME:-skillsync-backend}"; ALLOWED_ORIGINS="${ALLOWED_ORIGINS:-*}"; TABLE_NAME="${TABLE_NAME:-SkillSyncSkills}"
pushd backend >/dev/null
sam validate
sam build
sam deploy --stack-name "${STACK_NAME}" --resolve-s3 --capabilities CAPABILITY_IAM --parameter-overrides StageName=dev TableName="${TABLE_NAME}" AllowedOrigins="${ALLOWED_ORIGINS}" --region "${REGION}"
API_URL=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)
echo "API base URL: ${API_URL}"; echo "Set this in frontend/config.js as: window.API_BASE_URL = \"${API_URL}\""
popd >/dev/null
