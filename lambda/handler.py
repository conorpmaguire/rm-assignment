import json
import os
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    print("Lambda handler invoked")
    method = event.get("httpMethod")
    path = event.get("resource")

    try:
        if method == "POST" and path == "/upload":
            return upload_file(event)
        elif method == "GET" and path == "/files":
            return list_files()
        elif method == "GET" and path.startswith("/files/"):
            file_id = event["pathParameters"]["id"]
            return get_file(file_id)
        else:
            return response(404, {"error": "Not found"})
    except Exception as e:
        print("Error:", e)
        return response(500, {"error": "Internal server error", "details": str(e)})


def upload_file(event):
    print("Generate a presigned S3 upload URL and store file metadata")
    body = json.loads(event["body"])
    filename = body.get("filename")
    contentType = body.get("contentType")
    print("filename: ", filename)
    print("contentType: ", contentType)

    if not filename or not contentType:
        return response(400, {"error": "Missing filename or contentType"})

    file_id = str(uuid.uuid4())
    s3_key = f"uploads/{file_id}-{filename}"

    upload_url = s3.generate_presigned_post(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Fields={"Content-Type": contentType},
        Conditions=[
            ["content-length-range", 1, 20971520],  # 1 byte – 20 MB
            {"Content-Type": contentType}
        ],
        ExpiresIn=600
    )

    # Store initial metadata in DynamoDB
    metadata = {
        "id": file_id,
        "filename": filename,
        "s3Key": s3_key,
        "size": 0,
        "uploadTimestamp": datetime.utcnow().isoformat(),
    }

    table.put_item(Item=metadata)

    return response(200, {"id": file_id, "uploadURL": upload_url})

def list_files():
    print("List all files - metadata only")
    result = table.scan()
    items = result.get("Items", [])

    def replace_decimals(obj):
        if isinstance(obj, list):
            return [replace_decimals(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: replace_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        else:
            return obj

    clean_items = replace_decimals(items)
    return response(200, clean_items)

def get_file(file_id):
    print("Get file metadata and generate a presigned download URL")
    result = table.get_item(Key={"id": file_id})

    if "Item" not in result:
        return response(404, {"error": "File not found"})

    item = result["Item"]
    download_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": item["s3Key"]},
        ExpiresIn=300,
    )

    return response(200, {"id": item["id"], "filename": item["filename"], "downloadURL": download_url})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
