variable "aws_region" {
  type    = string
  default = "sa-east-1"
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
