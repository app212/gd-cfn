#!/usr/bin/env bash

STACK_NAME=$1

BUCKET_NAME="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "[Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue | [0]]" \
  --output text)"

aws s3 rm "s3://$BUCKET_NAME" --recursive

aws cloudformation delete-stack --stack-name $STACK_NAME