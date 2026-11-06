output "workspace" {
  value = terraform.workspace
}

output "instance_id" {
  value = aws_instance.app.id
}

output "instance_type" {
  value = aws_instance.app.instance_type
}
