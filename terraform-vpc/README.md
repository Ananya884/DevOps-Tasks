# Task 5: Provision a VPC with Terraform

Terraform code that creates an AWS VPC in `ap-south-1` with public and private subnets, an internet gateway, and route tables.

## Files

- `provider.tf`: Terraform and AWS provider setup
- `variables.tf`: region, project name, CIDR blocks, availability zones
- `main.tf`: VPC, internet gateway, subnets, route tables, associations
- `outputs.tf`: VPC ID and subnet IDs

## Architecture

- VPC: `10.0.0.0/16`
- Public subnets: `10.0.1.0/24` (ap-south-1a), `10.0.2.0/24` (ap-south-1b)
- Private subnets: `10.0.11.0/24` (ap-south-1a), `10.0.12.0/24` (ap-south-1b)
- Public route table sends `0.0.0.0/0` to the internet gateway
- Private route table has only the local route

## Usage

    terraform init
    terraform validate
    terraform plan
    terraform apply

## Result

`terraform apply` created 12 resources.

    private_subnet_ids = [
      "subnet-03dea8c004b94e9a9",
      "subnet-012de0d73f8eb146f",
    ]
    public_subnet_ids = [
      "subnet-043bca0e51fe98580",
      "subnet-00e5822cd0025b209",
    ]
    vpc_id = "vpc-0f5e867b49fea5daf"

## Cleanup

    terraform destroy
