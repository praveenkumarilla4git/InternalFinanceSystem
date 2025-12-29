provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_security_group" "web_firewall" {
  name        = "terraform-firewall"
  description = "Allow HTTP and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  # --- SCALE TO 3 SERVERS ---
  count = 3 

  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  # Attach the existing security group
  vpc_security_group_ids = [aws_security_group.web_firewall.id]

  # Dynamic Names: Finance-Server-1, Finance-Server-2, etc.
  tags = {
    Name = "Finance-Server-${count.index + 1}"
  }
}

# --- AUTOMATION: GENERATE ANSIBLE INVENTORY ---
resource "local_file" "ansible_inventory" {
  # This saves the file in the Ops-Config folder automatically
  filename = "../Ops-Config/inventory.ini" 
  
  # This Template fills in the new IP addresses automatically
  content  = <<EOT
[finance_servers]
${join("\n", aws_instance.app_server[*].public_ip)}

[finance_servers:vars]
ansible_user=ec2-user
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOT
}