#!/usr/bin/env bash

TMP_TEMPL=$(mktemp)
STACK_NAME=$1

awk '
/__CODE_PLACEHOLDER/ {
    while ((getline line < "func/index.py") > 0)
        print "          " line
    next
}
{ print }
' templates/main.yaml > $TMP_TEMPL


aws cloudformation deploy \
  --template-file "$TMP_TEMPL" \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_NAMED_IAM 

read -r BUCKET_NAME LB_DNS <<< "$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "[Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue | [0], Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue | [0]]" \
  --output text)"

aws s3 cp ./files/ "s3://$BUCKET_NAME/" --recursive

curl "http://$LB_DNS/?secret_key=secret1"