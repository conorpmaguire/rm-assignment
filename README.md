# RM Take Home Assignment - November 2025  

## Goal

> As a university professor, I want a simple way to share resource files with my students. Your task is to build a lightweight file-sharing API that supports uploads and downloads, stores files on disk, and makes it easy to retrieve shared files via a simple HTTP endpoint.

## Requirements

| Req # | Requirement | Description |
| --- | --- | ----------- |
| 1 | POST: Accepts a file upload (multipart/form-data). Returns a unique file ID or name used to retrieve it later |  |
| 2 | GET: Downloads the file associated with the given ID |  |
| 3 | GET: Lists all uploaded files (metadata only - no content) |  | 
| 4 | File Metadata to include File name, Size (in bytes), Upload timestamp, Unique ID |  | 
| 5 | No authentication required |  |
| 6 | Max file size: 20MB |  |
| 7 | What happens if something goes wrong during a request? How does the API communicate this to a client? |  |
| 8 | How can you confirm the code works? |  |
| 9 | How can someone else run and test the API quickly? |  |


## File Structure
```bash
.
├── .gitignore
├── README.md
├── ResMed_Assignment_1.pdf
├── lambda
│   ├── README.md
│   ├── requirements.txt
│   └── main.py
└── terraform
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── lambda.tf
```


## Design Decisions

| Design Decision | Justification |
| --- | ----------- |
| Scalability |  |
| Maintainability |  |
| Availability |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |


## Testing


## Use of AI
As the use of AI was encouraged for this assignment, I used Co-pilot and ChatGPT in the following ways:
- validating initial serverless technology choices
- calculating availability based on variety of AWS services used
- troubleshooting a run-time issue in Lambda handler concerning decimal formatting of values contained in file metadata
- validating and minor corrections of markdown documentation


## Assumptions

## Dependencies

## Caveats

## For the simplicity of having a single shared deployment process, Lambda functions are packaged and deployed via the Terraform config. In a production scenario, I would use the Serverless framework.


## Future Improvements


## Example Usage

**Build and deploy lambda **
```bash
cd lambda
pip install -r requirements.txt -t .
cd ../terraform
terraform init
terraform apply
```

### Obtain a presigned URL
```bash
curl -X POST https://hec8cyqmg5.execute-api.eu-west-1.amazonaws.com/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "RedMed_Assignment_1.pdf", "contentType": "application/pdf"}'
```

### Upload the file using the presigned URL
```bash
curl -X PUT -T RedMed_Assignment_1.pdf \
  -H "Content-Type: application/pdf" \
"https://resmed-fileshare-files.s3.amazonaws.com/uploads/da80df6f-005b-4e99-a565-470219267055-RedMed_Assignment_1.pdf?AWSAccessKeyId=ASIA5GWBOBYPDE4RIA6E&Signature=ZP9xdIeBAIo3qqFNbOQjjwFFdxo%3D&content-type=application%2Fpdf&x-amz-security-token=IQoJb3JpZ2luX2VjECYaCWV1LXdlc3QtMSJHMEUCIHV9T%2BjfGIlpaz44zQT44mnnI8IURniLGRewpzN4R2DAAiEAtrbzZUZJucDJlpDGp84CtVz7Tj0Vr7VSHDMCYAh4VQcq%2FQII3v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAEGgw5MDc3MTc1MTI3MzQiDICfR0BWfYmB8fWDNCrRAoxAF17JPZwPZTYfNOyl1Nzt8B9HTi3XQ8IINxu8rJJuFpFAErZfwEfDC%2BSsSG2ejWpdgxieFbW2k6EgMXcqHpmpX6HBOJ2thE5yzDI07KaQJQJhmKwWT%2FwH7tSFpsTWyAhQhs8wlqsAjor%2B8iKXrVIEceFZ%2BSbAkQhrKJAzwowSLO2lyek6EXzKCh2hLpsypuCLAng9MowH4fjxWl3qWGykSoPNAURQ9L0SmNssS1gIbIFqMipxelHUURh1KLhwyHf%2FLk9KCfBqoDRPRcK46yI8MB%2FywT9svAsbKSIaPVmyRlTkdAS22QkTwGbaGAEVcWJyH%2BtmDo4IwBFf%2BZgThQFu0qA0v%2BBps1oYn9w6qYVK8xUT1bg9y8SftsF89i2opdfRQFLSJiyVhySmaCRCo1XjvWVfOsZj5CXkm6qkFLW%2FzcDMzijbCcn44ERlDsUYn9IwjIaKyAY6ngG%2BwKuBYDlIvksel5bw2%2BYhbNMEpxV6vtGjJP%2FOEyOkq5CGjf9grbi92Kw0rjh46vQR%2BzoVEUEoE6kq0IKaVGU7DTixC257J6vLZsHKUH%2FpkyipnAOR9GE8UKemrs%2FfjDezpW0MLbXC6ooKRyBatkIlLglXXYwsf3BG4NQzuOpudFPf6t4fx44tdTNB9iYx2oluK8dZEvNoZBfBoI0iiQ%3D%3D&Expires=1761772601"
```

### List all files:
```bash
curl https://hec8cyqmg5.execute-api.eu-west-1.amazonaws.com/files
```

### Retrieve a file's metadata:
```bash
curl https://hec8cyqmg5.execute-api.eu-west-1.amazonaws.com/files/da80df6f-005b-4e99-a565-470219267055
```

### Get a presigned URL for downloading a file:
```bash
curl https://abc123.execute-api.us-east-1.amazonaws.com/files/uuid-1234
```
