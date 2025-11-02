import json
import os
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

# Initialize AWS SDK clients for S3 and DynamoDB
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Read environment variables for S3 bucket and DynamoDB table names
BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)  # Reference to the DynamoDB table


def lambda_handler(event, context):
    """
    Main Lambda handler function.
    Routes requests based on HTTP method and path.
    """
    print("Lambda handler invoked")

    method = event.get("httpMethod")
    path = event.get("resource")

    try:
        # Route POST requests to /upload
        if method == "POST" and path == "/upload":
            return upload_file(event)
        # Route GET requests to /files to list all files
        elif method == "GET" and path == "/files":
            return list_files()
        # Route GET requests to /files/{id} to retrieve a specific file
        elif method == "GET" and path.startswith("/files/"):
            file_id = event["pathParameters"]["id"]
            return get_file(file_id)
        # Catch-all for unsupported routes
        else:
            return response(404, {"error": "Not found"})
    except Exception as e:
        # Log unexpected errors and return 500
        print("Error:", e)
        return response(500, {"error": "Internal server error", "details": str(e)})


def upload_file(event):
    """
    Generates a presigned S3 POST URL for uploading a file
    and stores initial metadata in DynamoDB.
    """

    print("Generate a presigned S3 upload URL and store file metadata")

    # Parse request body JSON
    body = json.loads(event["body"])
    filename = body.get("filename")
    contentType = body.get("contentType")
    print("filename: ", filename)
    print("contentType: ", contentType)

    # Validate required fields
    if not filename or not contentType:
        return response(400, {"error": "Missing filename or contentType"})

    # Generate unique ID for the file
    file_id = str(uuid.uuid4())
    s3_key = f"uploads/{file_id}-{filename}"  # S3 key for file storage

    # Generate presigned POST URL for direct browser or client upload
    upload_url = s3.generate_presigned_post(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Fields={"Content-Type": contentType},
        Conditions=[
            ["content-length-range", 1, 20971520],  # Limit: 1 byte – 20 MB
            {"Content-Type": contentType}           # Enforce content type
        ],
        ExpiresIn=600  # URL expires in 10 minutes
    )

    # Store initial file metadata in DynamoDB
    metadata = {
        "id": file_id,
        "filename": filename,
        "s3Key": s3_key,
        "size": 0,  # Size will be updated after upload
        "uploadTimestamp": datetime.utcnow().isoformat(),
    }
    table.put_item(Item=metadata)

    # Return presigned URL and file ID to the client
    return response(200, {"id": file_id, "uploadURL": upload_url})


def list_files():
    """
    Returns a list of all uploaded file metadata.
    Converts DynamoDB Decimal types to int/float for JSON serialization.
    """
    print("List all files - metadata only")

    result = table.scan()          # Scan the DynamoDB table
    items = result.get("Items", [])

    # Helper function to convert Decimal objects to int/float
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
    """
    Retrieves metadata for a single file and generates a
    presigned S3 GET URL for downloading the file.
    """
    print("Get file metadata and generate a presigned download URL")

    result = table.get_item(Key={"id": file_id})

    if "Item" not in result:
        return response(404, {"error": "File not found"})

    item = result["Item"]

    # Generate presigned URL for temporary download access
    download_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": item["s3Key"]},
        ExpiresIn=300,  # URL expires in 5 minutes
    )

    return response(200, {"id": item["id"], "filename": item["filename"], "downloadURL": download_url})


def response(status_code, body):
    """
    Standardized HTTP response builder.
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
