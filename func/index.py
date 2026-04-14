import os
import json
import boto3

bucket_name = os.environ["BUCKET_NAME"]

secrets_client = boto3.client(service_name='secretsmanager')
s3_client = boto3.client(service_name='s3')


def lambda_handler(event, context):
    print("Event: ", event)
    print("Parameters: ", event.get("queryStringParameters"))
    try:
        query_params = event.get("queryStringParameters")
        secret_key = query_params.get("secret_key")

        if not secret_key:
            return {
                "statusCode": 400,
                "statusDescription": "400 Bad Request",
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Missing secret_key"
                })
            }
        print("Get secret")
        secret_response = secrets_client.get_secret_value(
            SecretId=secret_key
        )
        print("Secret retrieved")

        secret_value = secret_response["SecretString"]

        print("Reading bucket")
        s3_response = s3_client.list_objects_v2(
            Bucket=bucket_name
        )

        objects = [
            obj["Key"]
            for obj in s3_response.get("Contents", [])
        ]
        print("Objects list retrieved")

        return {
            "statusCode": 200,
            "statusDescription": "200 OK",
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "secret_value": secret_value,
                "bucket_objects": objects
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
