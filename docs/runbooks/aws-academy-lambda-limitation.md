# AWS Academy Lambda limitation

During the Phase 3 deployment validation, the serverless authentication
function could not be provisioned in the AWS Academy/Vocareum account because
the current lab role does not allow creating AWS Lambda functions.

Validated command:

```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account-id>:role/voclabs \
  --action-names lambda:CreateFunction \
  --resource-arns arn:aws:lambda:us-east-1:<account-id>:function:service-order-auth-cpf
```

Result:

```text
EvalActionName: lambda:CreateFunction
EvalDecision: implicitDeny
```

Impact:

- Terraform can package the Lambda artifact.
- Terraform can validate the infrastructure code.
- API Gateway resources may be created.
- The Lambda function itself cannot be created in this AWS Academy lab.

Because of that, the full serverless authorizer deployment is blocked by
the educational account policy, not by application code.

Mitigation for the academic demo:

- Keep the Lambda repository implemented, tested and validated.
- Keep Terraform code ready for an AWS account with Lambda permissions.
- Demonstrate the main application running on k3s with RDS.
- Document the intended architecture with API Gateway and Lambda Authorizer.
