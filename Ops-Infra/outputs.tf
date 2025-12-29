output "server_public_ip" {
  description = "The public IP address of the web server"
  value       = aws_instance.app_server.public_ip
}

output "server_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.app_server.id
}