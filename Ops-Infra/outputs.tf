output "server_ips" {
  description = "Public IPs of all 3 servers"
  value       = aws_instance.app_server[*].public_ip
}

output "server_ids" {
  description = "IDs of all 3 servers"
  value       = aws_instance.app_server[*].id
}