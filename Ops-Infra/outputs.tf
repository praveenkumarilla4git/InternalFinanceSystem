output "server_ips" {
  description = "Public IPs of all 3 servers"
  value       = aws_instance.app_server[*].public_ip
}

output "server_ids" {
  description = "IDs of all 3 servers"
  value       = aws_instance.app_server[*].id
}

output "alb_dns_name" {
  description = "The URL of the Load Balancer (Click this!)"
  value       = "http://${aws_lb.finance_alb.dns_name}"
}