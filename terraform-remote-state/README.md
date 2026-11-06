# Task 6: Remote State and Workspace Management

Terraform project that stores its state in an S3 backend with DynamoDB locking, and uses `dev` and `prod` workspaces with different instance sizes.

## Backend

- S3 bucket: `ananya-tf-state-668310558912` (versioning and encryption enabled)
- DynamoDB table: `terraform-locks` (partition key `LockID`)
- State key: `task6/terraform.tfstate`
- Each workspace gets its own state file under `env:/<workspace>/`

## Workspaces

| Workspace | Instance type |
|-----------|---------------|
| dev       | t3.micro      |
| prod      | t3.small      |

The size is chosen in `main.tf` with `lookup(var.instance_types, terraform.workspace, "t3.micro")`.

## Usage

    terraform init
    terraform workspace new dev
    terraform apply
    terraform workspace new prod
    terraform apply

## Result

- dev: `i-0e265c1e0be5be0f8` (t3.micro)
- prod: `i-0843d36ac51661955` (t3.small)

State files in S3:

    env:/dev/task6/terraform.tfstate
    env:/prod/task6/terraform.tfstate

## Cleanup

    terraform workspace select dev
    terraform destroy
    terraform workspace select prod
    terraform destroy
