#!/usr/bin/env bash
#
# Usage: ./upload.sh <filename> <content-type> <upload-api-url>
#
# Example:
#   ./upload.sh "ResMed_Assignment_1.pdf" "application/pdf" "https://abc.execute-api.eu-west-1.amazonaws.com/upload"
#
# Requirements:
#   - curl
#   - jq

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <filename> <content-type> <upload-api-url>"
  exit 1
fi

FILENAME="$1"
CONTENT_TYPE="$2"
BASE_URL="$3"

if [[ ! -f "$FILENAME" ]]; then
  echo "File not found: $FILENAME"
  exit 1
fi

# Automatically append /upload to the base URL
UPLOAD_URL="${BASE_URL%/}/upload"

echo "Requesting pre-signed URL from: $UPLOAD_URL"

echo "Requesting presigned URL from API..."
RESPONSE=$(curl -s -X POST "$UPLOAD_URL" \
  -H "Content-Type: application/json" \
  -d "{\"filename\": \"$(basename "$FILENAME")\", \"contentType\": \"$CONTENT_TYPE\"}")

# Check response
if [[ -z "$RESPONSE" ]] || ! echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
  echo "Invalid JSON response from API:"
  echo "$RESPONSE"
  exit 1
fi

URL=$(echo "$RESPONSE" | jq -r '.uploadURL.url')
FIELDS=$(echo "$RESPONSE" | jq -r '.uploadURL.fields | to_entries[] | "-F \(.key)=\(.value)"')

if [[ "$URL" == "null" ]]; then
  echo "Missing upload URL in response"
  echo "$RESPONSE"
  exit 1
fi

echo "Uploading '$FILENAME' to S3..."
# shellcheck disable=SC2086
eval curl -s -X POST "$URL" $FIELDS -F "file=@$FILENAME" > /dev/null

echo "Upload complete!"
