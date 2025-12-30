# --- 1. REMOTE STATE CONFIGURATION ---
terraform {
  backend "s3" {
    bucket         = "tf-state-praveen2-2025" 
    key            = "finance-system/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# --- 2. PROVIDER SETUP ---
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# --- 3. DATA SOURCES (Network Lookup) ---
# This automatically finds your default VPC and Subnets
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# --- 4. SECURITY GROUP (FIREWALL) ---
resource "aws_security_group" "web_firewall" {
  name        = "finance-app-firewall"
  description = "Allow HTTP and SSH"

  ingress { # SSH
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress { # Application Port (Variable)
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress { # ALB Port (Standard HTTP)
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress { # Outbound Internet
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- 5. SERVER FLEET ---
resource "aws_instance" "app_server" {
  count         = var.server_count
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.web_firewall.id]

  tags = {
    Name = "Finance-Server-${count.index + 1}"
  }
}

# --- 6. LOAD BALANCER CONFIGURATION ---

# Target Group: Defines "Where to send traffic" (Port 5000 on servers)
resource "aws_lb_target_group" "finance_tg" {
  name     = "finance-target-group"
  port     = var.app_port 
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
  
  health_check {
    path = "/" # Checks if homepage loads successfully
    port = var.app_port
  }
}

# Load Balancer: The "Front Door" (Listens on Port 80)
resource "aws_lb" "finance_alb" {
  name               = "finance-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_firewall.id]
  subnets            = data.aws_subnets.default.ids
}

# Listener: The "Bouncer" (Forwards Port 80 -> Target Group)
resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.finance_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.finance_tg.arn
  }
}

# Attachment: Connects the 3 Servers to the Target Group
resource "aws_lb_target_group_attachment" "finance_attach" {
  count            = var.server_count
  target_group_arn = aws_lb_target_group.finance_tg.arn
  target_id        = aws_instance.app_server[count.index].id
  port             = var.app_port
}

# --- 7. AUTOMATION: GENERATE ANSIBLE INVENTORY ---
resource "local_file" "ansible_inventory" {
  filename = "../Ops-Config/inventory.ini" 
  
  content  = <<EOT
[finance_servers]
${join("\n", aws_instance.app_server[*].public_ip)}

[finance_servers:vars]
ansible_user=ec2-user
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOT
}