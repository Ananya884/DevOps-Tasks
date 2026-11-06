data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = lookup(var.instance_types, terraform.workspace, "t3.micro")

  tags = {
    Name        = "${var.project_name}-${terraform.workspace}"
    Environment = terraform.workspace
  }
}
