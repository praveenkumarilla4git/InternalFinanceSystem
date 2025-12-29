
variable "aws_region" {
  description = "AWS Region to deploy to"
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "key_name" {
  description = "Name of the SSH key pair on AWS"
  default     = "batch3"
}

variable "ami_id" {
  description = "AMI ID for Amazon Linux 2023 (us-east-1)"
  default     = "ami-051f7e7f6c2f40dc1"
}

variable "instance_type" {
  description = "EC2 Instance Type (Select t2.micro or t3.micro for Free Tier)"
  default     = "t3.micro" 
}