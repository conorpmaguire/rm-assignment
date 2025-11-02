cd lambda
pip install -r requirements.txt -t .
cd ../terraform
terraform init
terraform apply



/usr/local/bin/python3



Risks

Assumptions

Dependencies

Caveats

For the simplicity of having a single shared deployment process, Lambda functions are packaged and deployed via the Terraform config. In a production scenario, I would use the Serverless framework.


Future Improvements
