variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "service-order"
}

variable "database_url" {
  type      = string
  sensitive = true
}

variable "customer_jwt_secret" {
  type      = string
  sensitive = true
}

variable "customer_jwt_issuer" {
  type    = string
  default = "service-order-auth-lambda/production"
}

variable "backend_base_url" {
  type = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by the Lambda to reach RDS."
  type        = list(string)
}

variable "lambda_security_group_ids" {
  description = "Security group IDs assigned to the Lambda. It must be allowed by the RDS security group on port 5432."
  type        = list(string)
}

variable "app_security_group_id" {
  description = "Deprecated compatibility variable. Use lambda_security_group_ids instead."
  type        = string
  default     = ""
}
