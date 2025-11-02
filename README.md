# RM Take Home Assignment - November 2025  

## Goal

> As a university professor, I want a simple way to share resource files with my students. Your task is to build a lightweight file-sharing API that supports uploads and downloads, stores files on disk, and makes it easy to retrieve shared files via a simple HTTP endpoint.

## Assignment Requirements

| Req # | Requirement | Description |
| --- | --- | ----------- |
| 1 | POST: Accepts a file upload (multipart/form-data). Returns a unique file ID or name used to retrieve it later | Implemented in Lambda handler path "/upload" https://github.com/conorpmaguire/rm-assignment/blob/05fa0a7fa7c49fb7d81a115e24f3e30d3c211cf3/lambda/handler.py#L22 |
| 2 | GET: Lists all uploaded files (metadata only - no content) | Implemented in Lambda handler path "/files" https://github.com/conorpmaguire/rm-assignment/blob/05fa0a7fa7c49fb7d81a115e24f3e30d3c211cf3/lambda/handler.py#L24 | 
| 3 | GET: Downloads the file associated with the given ID | Implemented in Lambda handler path "/files/{id}" https://github.com/conorpmaguire/rm-assignment/blob/05fa0a7fa7c49fb7d81a115e24f3e30d3c211cf3/lambda/handler.py#L26 |
| 4 | File Metadata to include File name, Size (in bytes), Upload timestamp, Unique ID | Metadata is stored in DynamoDB: https://github.com/conorpmaguire/rm-assignment/blob/05fa0a7fa7c49fb7d81a115e24f3e30d3c211cf3/lambda/handler.py#L62 | 
| 5 | No authentication required | No AWS credentials are needed locally — the pre-signed URL already contains temporary credentials. https://github.com/conorpmaguire/rm-assignment/blob/2bf665ae35236b4380d9295d8e4c2d3065c2faf6/lambda/handler.py#L50 |
| 6 | Max file size: 20MB | Achieved using a pre-signed POST URLs with a 'content-length-range' condition https://github.com/conorpmaguire/rm-assignment/blob/2bf665ae35236b4380d9295d8e4c2d3065c2faf6/lambda/handler.py#L55 |
| 7 | What happens if something goes wrong during a request? How does the API communicate this to a client? | The server will return an error code if something goes wrong. A "404" error is returned if no HTTP method is supplied. A generic "500" error, along with a specific error message, is returned if the server fails. |
| 8 | How can you confirm the code works? | Code was fully tested end-to-end using the test steps outlined below. |
| 9 | How can someone else run and test the API quickly? | Please follow the steps contained in the "Installation" section below. https://github.com/conorpmaguire/rm-assignment/blob/2bf665ae35236b4380d9295d8e4c2d3065c2faf6/lambda/handler.py#L33 |


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
| Simplicity | For the simplicity of having a single shared deployment process, Lambda functions are packaged and deployed via the Terraform config. In a production scenario, I would use the Serverless framework. |
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
- creating an upload script to eliminate need to copy/paste tokens and URLs between curl commands


## Assumptions

## Dependencies

## Caveats



## Future Improvements

- Manage Terraform state remotely
- Proper test framework


## Installation

## Step 1 - Build Lambda Function & Other Infrastructure
```bash
cd lambda
pip install -r requirements.txt -t .
cd ../terraform
terraform init
terraform apply
```
** Note the API endpoint URL that is output after the Terraform config is applied - this URL is used in subsequent commands **
```bash
api_endpoint = "https://smwrz81zqf.execute-api.eu-west-1.amazonaws.com"
```


## Step 2a - UPLOAD - Run the Upload Script (the easy option!)
```bash
./upload.sh "ResMed_Assignment_1.pdf" "application/pdf" "https://smwrz81zqf.execute-api.eu-west-1.amazonaws.com"
```


## Step 2b UPLOAD (Alternative) - Run the curl commands separately (cumbersome and error-prone!)

### Obtain a presigned URL
```bash
curl -X POST https://smwrz81zqf.execute-api.eu-west-1.amazonaws.com/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "ResMed_Assignment_1.pdf", "contentType": "application/pdf"}'
```

### Upload the file using the presigned URL
```bash
curl -X POST https://resmed-fileshare-files.s3.amazonaws.com/ \
  -F "key=uploads/82bd10cf-cb4b-4c4f-b3e1-b086a0bc138c-ResMed_Assignment_1.pdf" \
  -F "Content-Type=application/pdf" \
  -F "AWSAccessKeyId=ASIA5GWBOBYPCKBM2PMF" \
  -F "x-amz-security-token=IQoJb3JpZ2luX2VjEIL//////////wEaCWV1LXdlc3QtMSJGMEQCIEnv3F6JXS9FQnhfqR1rC1zKQsLEhvnd2U3G3qLZxLakAiB8FpoiHDBRgD6JE4sxZ/ZSs80p+V0dTFDucax0U5DcHir0AghLEAQaDDkwNzcxNzUxMjczNCIMP8jhFI4xwpUC78tPKtEC7ojXdEKOU0tIomqqxG6GY1gP72beW4wXeV5WiSPgTiK+/qjPDtynI0s2hL1RUDQUNaf5PhI35PShLxBl4AeEokpOp1wh28WzsOMZFGXRd1IMUetQQmvzXetNo5Vh5zO6lD//ygK1/W7QOJUyT+mn7Xz5zhpbsmPfU8UVKaBN+n5iU+nYUa5R5AjsxYmFb3BTbJyizXc/pS+AvQgNDpXl6RgARWM+TNhdgi5qxb98blp2UV3d4ZTKZovZwMXgIxLwdDx+EqtxQy+Kr2MBCFSz/hHHAD+46Q9m89Tx0qrjcB8I1K4vnG4X46SJ16GtPyI4E4Q9bfaAck87frc182VmOBi1zcIHk3UvFyKAJnEWd6+oMtpXq7ZwFHzWav7NBYVMncMXyeBYyJOgJgVJB7f5dIi+EUhnNXj6IKVG6s+c2hNeRWqIBwTibSpTEc1v5e9kxjC/q57IBjqfASpaRAiGvvLdM82vwk69LbiN6atH3of3UUO7o5CY1r3vmwh5Avu3Dxlc2wYLgAW0OLIsd1h4YYpkq6OQd24p6s72K7ZrxA8QYVS3GGZ5tr+porL8Le5KEsew1AKiDoT4o10GWj8GPFiePfghLCHketL1poNPGEosVUumYa6M3bS3Q4pNAVHaeIL3DEjoQexIsmsGeN9HGVTKNcXjExOWlA==" \
  -F "policy=eyJleHBpcmF0aW9uIjogIjIwMjUtMTEtMDJUMTc6Mzc6NDdaIiwgImNvbmRpdGlvbnMiOiBbWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsIDEsIDIwOTcxNTIwXSwgeyJDb250ZW50LVR5cGUiOiAiYXBwbGljYXRpb24vcGRmIn0sIHsiYnVja2V0IjogInJlc21lZC1maWxlc2hhcmUtZmlsZXMifSwgeyJrZXkiOiAidXBsb2Fkcy84MmJkMTBjZi1jYjRiLTRjNGYtYjNlMS1iMDg2YTBiYzEzOGMtUmVzTWVkX0Fzc2lnbm1lbnRfMS5wZGYifSwgeyJ4LWFtei1zZWN1cml0eS10b2tlbiI6ICJJUW9KYjNKcFoybHVYMlZqRUlMLy8vLy8vLy8vL3dFYUNXVjFMWGRsYzNRdE1TSkdNRVFDSUVudjNGNkpYUzlGUW5oZnFSMXJDMXpLUXNMRWh2bmQyVTNHM3FMWnhMYWtBaUI4RnBvaUhEQlJnRDZKRTRzeFovWlNzODBwK1YwZFRGRHVjYXgwVTVEY0hpcjBBZ2hMRUFRYUREa3dOemN4TnpVeE1qY3pOQ0lNUDhqaEZJNHh3cFVDNzh0UEt0RUM3b2pYZEVLT1UwdElvbXFxeEc2R1kxZ1A3MmJlVzR3WGVWNVdpU1BnVGlLKy9xalBEdHluSTBzMmhMMVJVRFFVTmFmNVBoSTM1UFNoTHhCbDRBZUVva3BPcDF3aDI4V3pzT01aRkdYUmQxSU1VZXRRUW12elhldE5vNVZoNXpPNmxELy95Z0sxL1c3UU9KVXlUK21uN1h6NXpocGJzbVBmVThVVkthQk4rbjVpVStuWVVhNVI1QWpzeFltRmIzQlRiSnlpelhjL3BTK0F2UWdORHBYbDZSZ0FSV00rVE5oZGdpNXF4Yjk4YmxwMlVWM2Q0WlRLWm92WndNWGdJeEx3ZER4K0VxdHhReStLcjJNQkNGU3ovaEhIQUQrNDZROW04OVR4MHFyamNCOEkxSzR2bkc0WDQ2U0oxNkd0UHlJNEU0UTliZmFBY2s4N2ZyYzE4MlZtT0JpMXpjSUhrM1V2RnlLQUpuRVdkNitvTXRwWHE3WndGSHpXYXY3TkJZVk1uY01YeWVCWXlKT2dKZ1ZKQjdmNWRJaStFVWhuTlhqNklLVkc2cytjMmhOZVJXcUlCd1RpYlNwVEVjMXY1ZTlreGpDL3E1N0lCanFmQVNwYVJBaUd2dkxkTTgydndrNjlMYmlONmF0SDNvZjNVVU83bzVDWTFyM3Ztd2g1QXZ1M0R4bGMyd1lMZ0FXME9MSXNkMWg0WVlwa3E2T1FkMjRwNnM3Mks3WnJ4QThRWVZTM0dHWjV0citwb3JMOExlNUtFc2V3MUFLaURvVDRvMTBHV2o4R1BGaWVQZmdoTENIa2V0TDFwb05QR0Vvc1ZVdW1ZYTZNM2JTM1E0cE5BVkhhZUlMM0RFam9RZXhJc21zR2VOOUhHVlRLTmNYakV4T1dsQT09In1dfQ==" \
  -F "signature=XF9RFzLW0lG2d5eKx5eA9tIC1n4=" \
  -F "file=@ResMed_Assignment_1.pdf"
```


### Upload the file using the presigned URL
```bash
curl -X PUT -T ResMed_Assignment_1.pdf \
  -H "Content-Type: application/pdf" \
"https://resmed-fileshare-files.s3.amazonaws.com/uploads/da80df6f-005b-4e99-a565-470219267055-RedMed_Assignment_1.pdf?AWSAccessKeyId=ASIA5GWBOBYPDE4RIA6E&Signature=ZP9xdIeBAIo3qqFNbOQjjwFFdxo%3D&content-type=application%2Fpdf&x-amz-security-token=IQoJb3JpZ2luX2VjECYaCWV1LXdlc3QtMSJHMEUCIHV9T%2BjfGIlpaz44zQT44mnnI8IURniLGRewpzN4R2DAAiEAtrbzZUZJucDJlpDGp84CtVz7Tj0Vr7VSHDMCYAh4VQcq%2FQII3v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAEGgw5MDc3MTc1MTI3MzQiDICfR0BWfYmB8fWDNCrRAoxAF17JPZwPZTYfNOyl1Nzt8B9HTi3XQ8IINxu8rJJuFpFAErZfwEfDC%2BSsSG2ejWpdgxieFbW2k6EgMXcqHpmpX6HBOJ2thE5yzDI07KaQJQJhmKwWT%2FwH7tSFpsTWyAhQhs8wlqsAjor%2B8iKXrVIEceFZ%2BSbAkQhrKJAzwowSLO2lyek6EXzKCh2hLpsypuCLAng9MowH4fjxWl3qWGykSoPNAURQ9L0SmNssS1gIbIFqMipxelHUURh1KLhwyHf%2FLk9KCfBqoDRPRcK46yI8MB%2FywT9svAsbKSIaPVmyRlTkdAS22QkTwGbaGAEVcWJyH%2BtmDo4IwBFf%2BZgThQFu0qA0v%2BBps1oYn9w6qYVK8xUT1bg9y8SftsF89i2opdfRQFLSJiyVhySmaCRCo1XjvWVfOsZj5CXkm6qkFLW%2FzcDMzijbCcn44ERlDsUYn9IwjIaKyAY6ngG%2BwKuBYDlIvksel5bw2%2BYhbNMEpxV6vtGjJP%2FOEyOkq5CGjf9grbi92Kw0rjh46vQR%2BzoVEUEoE6kq0IKaVGU7DTixC257J6vLZsHKUH%2FpkyipnAOR9GE8UKemrs%2FfjDezpW0MLbXC6ooKRyBatkIlLglXXYwsf3BG4NQzuOpudFPf6t4fx44tdTNB9iYx2oluK8dZEvNoZBfBoI0iiQ%3D%3D&Expires=1761772601"
```


## Step 3 - LIST - List all files
```bash
curl https://smwrz81zqf.execute-api.eu-west-1.amazonaws.com/files
```


## Step 4 - LIST - Get file metadata and generate a presigned download URL:
```bash
curl https://smwrz81zqf.execute-api.eu-west-1.amazonaws.com/files/da80df6f-005b-4e99-a565-470219267055
```
