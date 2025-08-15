#!/usr/bin/env bash
set -euo pipefail
REGION="${AWS_REGION:-us-east-1}"; STACK_NAME="${STACK_NAME:-skillsync-frontend}"; SITE_BUCKET="${SITE_BUCKET:?Please provide SITE_BUCKET env var for S3 bucket name}"
aws cloudformation deploy --template-file infra/frontend.yaml --stack-name "${STACK_NAME}" --parameter-overrides SiteBucketName="${SITE_BUCKET}" --capabilities CAPABILITY_NAMED_IAM --region "${REGION}"
BUCKET=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
DIST_ID=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" --query "Stacks[0].Outputs[?OutputKey=='DistributionId'].OutputValue" --output text)
DIST_DOMAIN=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" --query "Stacks[0].Outputs[?OutputKey=='DistributionDomainName'].OutputValue" --output text)
aws s3 sync frontend/ "s3://${BUCKET}" --delete
aws cloudfront create-invalidation --distribution-id "${DIST_ID}" --paths "/*" >/dev/null
echo "Frontend deployed at: https://${DIST_DOMAIN}"
