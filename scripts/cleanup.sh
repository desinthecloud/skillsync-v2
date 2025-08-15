#!/usr/bin/env bash
set -euo pipefail
REGION="${AWS_REGION:-us-east-1}"
sam delete --stack-name skillsync-backend --region "${REGION}" || true
STACK=skillsync-frontend
BUCKET=$(aws cloudformation describe-stacks --stack-name "${STACK}" --region "${REGION}" --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text 2>/dev/null || true)
if [[ -n "${BUCKET}" ]]; then aws s3 rm "s3://${BUCKET}" --recursive || true; fi
aws cloudformation delete-stack --stack-name "${STACK}" --region "${REGION}" || true
echo "Requested deletion of ${STACK}."
